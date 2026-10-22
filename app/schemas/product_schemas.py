from pydantic import BaseModel, Field, ConfigDict

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
