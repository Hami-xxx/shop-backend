from models import User
from auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
def create_user(
    user,
    db
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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
        raise HTTPException(status_code=404,detail="User not found")
    
    if user_db.id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")

    user_db.username=user.username

    db.commit()
    db.refresh(user_db)
    return user_db

def delete_user(
    id,
    db
):
    user_db = db.get(User,id)

    if not user_db:
        raise HTTPException(status_code=404,detail="User not found")
    
    db.delete(user_db)
    db.commit()

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
        raise HTTPException(status_code=404,detail="Username wrrong")
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
        raise HTTPException(status_code=401,detail="Password wrong")
