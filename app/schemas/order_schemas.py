from pydantic import BaseModel, Field, ConfigDict

from enum import Enum

from app.schemas.product_schemas import ProductResponse
from app.schemas.user_schemas import UserResponse

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
