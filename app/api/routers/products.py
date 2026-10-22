from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.services import products_service
from app.schemas.product_schemas import CreateProduct, UpdateProduct, ProductResponse
from app.core.auth import get_current_admin
from app.core.dependecies import get_db 

router = APIRouter()

@router.post("/admin/products",summary="Create Product",description="Only admin can create product")
def create_product(
    product : CreateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.create_product(
        product=product,
        current_admin=current_admin,
        db=db
    )

@router.get("/products", response_model=list[ProductResponse],summary="Get products")
def get_products(
    db : Session=Depends(get_db)
):
    return products_service.get_products(
        db=db
    )

@router.put("/admin/products/{id}",summary="Change stock of product",description="Only admin can update product")
def update_stock(
    id : int,
    product : UpdateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.update_stock(
        id=id,
        product=product,
        db=db,
        current_admin=current_admin
    )

@router.delete("/admin/products/{id}",summary="Delete product",description="Only admin can delete product")
def delete_prodcut(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.delete_product(
        id=id,
        db=db,
        current_admin=current_admin
    )    
