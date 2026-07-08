from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import users_service
from auth import get_current_admin, get_current_user
from schemas import CreateUser, UserResponse, UpdateUser, LoginUser
from dependecies import get_db 

router = APIRouter()


@router.post("/users",response_model=UserResponse)
def create_user(
    user : CreateUser,
    db : Session=Depends(get_db)
):
    return users_service.create_user(
        user=user,
        db=db
    )

@router.get("/users",response_model=list[UserResponse])
def get_users(
    db : Session=Depends(get_db)
):
    return users_service.get_users(
        db=db
    )

@router.put("/users/{id}",response_model=UserResponse)
def update_user(
    id : int,
    user : UpdateUser,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return users_service.update_user(
        id=id,
        user=user,
        current_user=current_user,
        db=db
    )

@router.delete("/users/{id}")
def delete_user(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return users_service.delete_user(
        id=id,
        db=db
    )

@router.post("/login")
def login(
    user : LoginUser,
    db : Session=Depends(get_db)
):
    return users_service.login(
        user=user,
        db=db
    )
@router.get("/me",response_model=UserResponse)
def profile(
    current_user=Depends(get_current_user)
):
    return current_user