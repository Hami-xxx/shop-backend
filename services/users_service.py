from models import User
from auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from exceptions.errors import UserNotFound, AccessDenied
import logging

logger = logging.getLogger(__name__)

def create_user(
    user,
    db
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(
            "User created",
            extra={
                "username" : user.username,
                "user_email" : user.email 
            }
        )
        

    except Exception:
        db.rollback()
        logger.exception(
            "User created failed",
            extra={
                "username" : user.username,
                "user_email" : user.email
            }
        )
        raise
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

    user_db.username=user.username
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
    current_admin
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
            "User deleted by admin",
            extra={
                "user_id" : id,
                "admin_id" : current_admin.id
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
            "User failed login",
            extra={
                "user_id" : user_db.id
            }
        )
        raise HTTPException(status_code=404,detail="Invalid username or password")
    elif verify_password(user.password,user_db.password):
        token = create_access_token(
            {
                "sub" : str(user_db.id),
                "role" : user_db.role
            }
        )
        return {
            "access_token" : token,
            "token_type" : "bearer"
        }
    else:
        logger.error(
        "User failed login",
            extra={
                "user_id" : user_db.id
            }
    )
        raise HTTPException(status_code=401,detail="Invalid username or password")
