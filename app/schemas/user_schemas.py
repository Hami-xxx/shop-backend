from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
class Role(str,Enum):
    admin = "admin"
    user = "user"

class CreateUser(BaseModel):
    username : str = Field(min_length=1)
    email : EmailStr | None = None
    password : str = Field(min_length=8)

class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr
    role : Role

    model_config = ConfigDict(
        from_attributes=True
    )
    
class UpdateUser(BaseModel):
    username : str | None = None
    email : EmailStr | None = None

class LoginUser(BaseModel):
    username : str = Field(min_length=1,max_length=30)
    password : str = Field(min_length=8,max_length=20)

class ChangeRole(BaseModel):
    email : EmailStr
    role : Role

class RefreshTokenRequest(BaseModel):
    token : str = Field(min_length=40)