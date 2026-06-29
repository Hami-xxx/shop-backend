from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from schemas import CreateProduct, UpdateProduct
from auth import get_current_admin
from dependecies import get_db 

router = APIRouter()

@router.post("/products/admin")
def create_product(
    product : CreateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/products")
def get_products(
    db : Session=Depends(get_db)
    ):
   
    return db.query(Product).all()

@router.put("/products/admin/{id}")
def update_stock(
    id : int,
    product : UpdateProduct,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    product_db = db.get(Product,id)
    if not product_db:
        raise HTTPException(status_code=404,detail="Product not found")
    
    product_db.stock+=product.stock
    db.commit()
    db.refresh(product_db)

    return product_db

@router.delete("/products/admin/{id}")
def delete_prodcut(
    id : int,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    product_db = db.get(Product,id)
    if not product_db:
        raise HTTPException(status_code=404,detail="Product not found")
    
    db.delete(product_db)
    db.commit()

    
    return {
        "message" : "Deleted successfully"
    }
    
