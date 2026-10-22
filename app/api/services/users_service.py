from app.db.models import User, RefreshToken
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token, hash_refresh_token
from app.exceptions.errors import UserNotFound, AccessDenied

from fastapi import HTTPException

from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

import logging

logger = logging.getLogger(__name__)

def create_user(
    user,
    db
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role = user.role
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(
            "User created",
            extra={
                "user_id" : new_user.id,
                "username" : new_user.username,
                "user_email" : new_user.email 
            }
        )
    except IntegrityError as e:
        db.rollback()
        logger.warning(
            "User creation failed due to integrity error (likely duplicate username/email)",
            extra={
                "username": user.username,
                "email": user.email,
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    except Exception as e:
        db.rollback()
        logger.exception(
            "Unexpected error during user creation",
            extra={
                "username": user.username,
                "error": str(e)
            }
        )
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred"
        )    
    return new_user

def get_users(
    db
):
    return db.query(User).all()

def update_user(
    id,
    user,
    current_user,
    db
):
    user_db = db.get(User,id)
    if not user_db:
        logger.error(
            "User Not found",
            extra={
                "user_id" : id
            }
        )
        raise UserNotFound()
    
    if user_db.id != current_user.id:
        logger.warning(
            "Access denied",
            extra={
                "user_id" : current_user.id
            }
        )
        raise AccessDenied()

    change = False
    if user.username is not None:
        user_db.username=user.username
        change=True

    if user.email is not None:
        user_db.email=user.email
        change=True

    if not change:
        raise HTTPException(
        status_code=409,
        detail="Please change username or email"
    )

    try:
        db.commit()
        db.refresh(user_db)
        logger.info(
            "User change username",
            extra={
                "user_id" : id
            }
        )
    except Exception:
        db.rollback()
        logger.exception(
            "User failed to change username",
            extra={
                "user_id" : id
            }
        )
        raise
    return user_db

def delete_user(
    id,
    db,
):
    user_db = db.get(User,id)

    if not user_db:
        logger.error(
            "User not found",
            extra={
                "user_id" : id
            }
        )
        raise UserNotFound()
    try:
        db.delete(user_db)
        db.commit()
        logger.info(
            "User deleted",
            extra={
                "user_id" : id
            }
        )
    except Exception:
        db.rollback()
        logger.exception(
            "User failed delete",
            extra={
                "user_id" : id
            }
        )

    return {
        "message" : "Deleted successfully"
    }

def login(
    user,
    db
):
    user_db = db.query(User).filter_by(
        username=user.username
    ).first()

    if not user_db:
        logger.error(
            "Username not found",
            extra={
                "username" : user.username
            }
        )
        raise HTTPException(status_code=401,detail="Invalid username or password")
    if verify_password(user.password,user_db.password):
        token = create_access_token(
            {
                "sub" : str(user_db.id),
                "role" : user_db.role
            }
        )
        refresh_token = create_refresh_token()
        refresh_token_hash = hash_refresh_token(refresh_token)
        refresh = RefreshToken(
            user_id=user_db.id,
            token_hash=refresh_token_hash,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        try:
            db.add(refresh)
            db.commit()
            db.refresh(refresh)
            logger.info(
                "User login",
                extra={
                    "user_id" : user_db.id
                }
            )
        except Exception:
            db.rollback()
            logger.exception(
                "User failed login",
                extra={
                    "user_id" : user_db.id
                }
            )
            raise
        return {
            "access_token" : token,
            "refresh_token" : refresh_token,
            "token_type" : "bearer"
        }
    else:
        logger.error(
            "Password wrong",
            extra={
                "user_id" : user_db.id
            }
    )
        raise HTTPException(status_code=401,detail="Invalid username or password")

def refresh(
    refresh_token,
    db
):
    token_hash = hash_refresh_token(refresh_token.token)

    refresh_db = db.query(RefreshToken).with_for_update().filter_by(
        token_hash=token_hash
    ).first()

    if not refresh_db:
        logger.warning(
            "Invalid refresh token"
        )
        raise HTTPException(
        status_code=401,
        detail="Invalid refresh token"
    )

    if refresh_db.expires_at < datetime.utcnow():
        logger.error(
            "Refresh token expired",
            extra={
                "user_id" : refresh_db.user.id,
                "refresh_id" : refresh_db.id
            }
        )
        db.delete(refresh_db)
        db.commit()
        raise HTTPException(
        status_code=401,
        detail="Refresh token expired"
    )   
        
    access_token = create_access_token(
        {
            "sub" : str(refresh_db.user.id),
            "role" : refresh_db.user.role
        }
    )
    refresh_token = create_refresh_token()
    refresh_token_hash= hash_refresh_token(refresh_token)
    refresh = RefreshToken(
        user_id=refresh_db.user.id,
        token_hash=refresh_token_hash,
        expires_at=datetime.utcnow() + timedelta(days=30)
        )
    try:
        db.add(refresh)
        db.delete(refresh_db)
        db.commit()
        db.refresh(refresh)
        logger.info(
            "New Refresh token created",
            extra={
                "user_id" : refresh.user_id,
                "refresh_id" : refresh.id
                }
            )
        logger.info(
            "Created access token",
            extra={
                "user_id" : refresh_db.user.id
            }
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Refresh token failed token",
            extra={
                "user_id" : refresh.user_id,
                "refresh_id" : refresh.id
                }
            )
        raise
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }

def logout(
    refresh_token,
    db
):

    token_hash = hash_refresh_token(refresh_token.token)

    refresh_db = db.query(RefreshToken).with_for_update().filter_by(
        token_hash=token_hash
    ).first()

    if not refresh_db:
            logger.warning(
                "Invalid refresh token"
            )
            raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    user_id = refresh_db.user.id
    refresh_id = refresh_db.id
    if refresh_db.expires_at < datetime.utcnow():
        logger.error(
            "Refresh token expired",
            extra={
            "user_id" : user_id,
            "refresh_id" : refresh_id
            }
        )
        raise HTTPException(
        status_code=401,
        detail="Refresh token expired"
        )   
    try:
        db.delete(refresh_db)
        db.commit()
        logger.info(
            "Logout successfully",
            extra={
                "user_id" : user_id,
                "refresh_id" : refresh_id
            }
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Logout failed",
            extra={
                "user_id" : user_id,
                "refresh_id" : refresh_id
            }
        )
        raise

    return {
        "message" : "Logout successfully"
    }