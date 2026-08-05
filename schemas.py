from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
#User
class Role(str,Enum):
    admin = "admin"
    user = "user"

class CreateUser(BaseModel):
    username : str = Field(min_length=1)
    email : EmailStr | None = None
    password : str = Field(min_length=8)
    role : Role 

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
#Product
class CreateProduct(BaseModel):
    name : str = Field(min_length=1)
    price : int = Field(gt=0)
    stock : int = Field(gt=0)

class UpdateProduct(BaseModel):
    stock : int = Field(gt=0)

class ProductResponse(BaseModel):
    id : int
    name : str
    price : int
    stock : int
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
    product_id : int = Field(gt=0)
    quantity : int = Field(gt=0)

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
    status : OrderStatus
    model_config = ConfigDict(
        from_attributes=True
    )

class RefreshTokenRequest(BaseModel):
    token : str = Field(min_length=40)