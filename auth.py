from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from dependecies import get_db
from models import User
pwd_context =CryptContext(
    schemes=["bcrypt"]
)
SECRET_KEY = "my_super_secret_key"
ALRGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
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
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES                                    
    )
    to_encode.update(
        {
            "exp" : expire
        }
    )
    encode_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALRGORITHM
    )
    
    return encode_jwt

def verify_token(
        token : str
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALRGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
            )
def get_current_user(
        token : str=Depends(oauth2_scheme),
        db : Session=Depends(get_db)
):
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token!"
        )
    user = db.get(User,int(user_id))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Inavlid Token"
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