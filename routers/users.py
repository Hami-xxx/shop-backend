from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import CreateUser, UserResponse, UpdateUser, LoginUser
from auth import hash_password, verify_password, create_access_token, verify_token, get_current_user, get_current_admin
from dependecies import get_db 

router = APIRouter()


@router.post("/users",response_model=UserResponse)
def create_user(
    user : CreateUser,
    db : Session=Depends(get_db)
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
@router.get("/users",response_model=list[UserResponse])
def get_users(
    db : Session=Depends(get_db)
):
    return db.query(User).all()

@router.put("/users/{id}",response_model=UserResponse)
def update_user(
    id : int,
    user : UpdateUser,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
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

@router.delete("/users/{id}")
def delete_user(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    user_db = db.get(User,id)

    if not user_db:
        raise HTTPException(status_code=404,detail="User not found")
    
    db.delete(user_db)
    db.commit()

    return {
        "message" : "Deleted successfully"
    }

@router.post("/login")
def login(
    user : LoginUser,
    db : Session=Depends(get_db)
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
@router.get("/me",response_model=UserResponse)
def profile(
    current_user=Depends(get_current_user)
):
    return current_user