from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
#User
class Role(str,Enum):
    admin = "admin"
    user = "user"

class CreateUser(BaseModel):
    username : str
    email : EmailStr
    password : str = Field(min_length=8,max_length=20)
    role : Role 

class UserResponse(BaseModel):
    username : str
    email : EmailStr

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

class ProductResponse(BaseModel):
    name : str
    price : int
    model_config = ConfigDict(
        from_attributes=True
    ) 
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

class OrderItemsRespone(BaseModel):
    quantity : int
    product : ProductResponse
    model_config = ConfigDict(
        from_attributes=True
    )

class OrderRespone(BaseModel):
    id : int
    user : UserResponse
    items : list[OrderItemsRespone]
    status : str
    model_config = ConfigDict(
        from_attributes=True
    )