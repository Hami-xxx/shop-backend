from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
#User
class CreateUser(BaseModel):
    username : str
    email : EmailStr
    password : str = Field(min_length=8,max_length=20)
    role : str = Field(default="user")

class UserResponse(BaseModel):
    username : str
    email : EmailStr
    role : str 

    model_config = ConfigDict(
        from_attributes=True
    )
    
class UpdateUser(BaseModel):
    username : str

class LoginUser(BaseModel):
    username : str
    password : str
#Product
class CreateProduct(BaseModel):
    name : str
    price : int
    stock : int

class UpdateProduct(BaseModel):
    stock : int
#order
class OrderStatus(str,Enum):
    pending = "pending"
    paid = "paid"
    sending = "sending"
    delivered = "delivered"

class UpdateStatus(BaseModel):
    status : OrderStatus

class OrderItems(BaseModel):
    product_id : int
    quantity : int