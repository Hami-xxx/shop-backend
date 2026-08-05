from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from core.dependecies import get_db
from db.models import User
from core.config import settings
import secrets
import hashlib
pwd_context =CryptContext(
    schemes=["bcrypt"]
)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(
        plain_password : str,
        hashd_password : str
):
    return pwd_context.verify(
        plain_password,
        hashd_password
    )

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES                                   
    )
    to_encode.update(
        {
            "exp" : expire
        }
    )
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encode_jwt

def verify_token(
        token : str
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
            )
def create_refresh_token():
    return secrets.token_urlsafe(64)
def hash_refresh_token(token : str):
    return hashlib.sha256(
        token.encode()
    ).hexdigest()

def get_current_user(
        token : str=Depends(oauth2_scheme),
        db : Session=Depends(get_db)
):
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    user = db.get(User,int(user_id))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return user

def get_current_admin(
        current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    return current_user