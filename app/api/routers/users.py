from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.services import users_service
from app.core.auth import get_current_admin, get_current_user
from app.schemas.user_schemas import CreateUser, UserResponse, UpdateUser, LoginUser, RefreshTokenRequest
from app.core.dependecies import get_db 

router = APIRouter()


@router.post("/users",response_model=UserResponse,summary="Create user")
def create_user(
    user : CreateUser,
    db : Session=Depends(get_db)
):
    return users_service.create_user(
        user=user,
        db=db
    )

@router.get("/admin/users",response_model=list[UserResponse],summary="Get Users",description="Only admin can get users")
def get_users(
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)

):
    return users_service.get_users(
        db=db
    )

@router.put("/users/{id}",response_model=UserResponse,summary="Change profile",description="Only change username or email")
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

@router.delete("/users/{id}",summary="Delete user",description="Only admin can delete user")
def delete_user(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return users_service.delete_user(
        id=id,
        db=db
    )

@router.post("/login",summary="Login to account")
def login(
    user : LoginUser,  
    db : Session=Depends(get_db)
):
    return users_service.login(
        user=user,
        db=db
    )
@router.get("/me",response_model=UserResponse,summary="Get profile",description="Get profile with current user")
def profile(
    current_user=Depends(get_current_user)
):
    return current_user

@router.post("/refresh",summary="Create refresh token")
def refresh(
    refresh_token : RefreshTokenRequest,
    db : Session=Depends(get_db)
):
    return users_service.refresh(
        refresh_token=refresh_token,
        db=db
    )

@router.post("/logout",summary="Logout account")
def logout(
    refresh_token : RefreshTokenRequest,
    db : Session=Depends(get_db)
):
    return users_service.logout(
        refresh_token=refresh_token,
        db=db
    )