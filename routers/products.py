from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import products_service
from schemas import CreateProduct, UpdateProduct, ProductResponse
from auth import get_current_admin
from dependecies import get_db 

router = APIRouter()

@router.post("/admin/products")
def create_product(
    product : CreateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.create_product(
        product=product,
        db=db
    )

@router.get("/products", response_model=list[ProductResponse])
def get_products(
    db : Session=Depends(get_db)
):
    return products_service.get_products(
        db=db
    )

@router.put("/admin/products/{id}")
def update_stock(
    id : int,
    product : UpdateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.update_stock(
        id=id,
        product=product,
        db=db
    )

@router.delete("/admin/products/{id}")
def delete_prodcut(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return products_service.delete_product(
        id=id,
        db=db
    )    
