from models import Product
from fastapi import HTTPException
def create_product(
    product,
    db
    
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

def get_products(
    db
):
    return db.query(Product).all()

def update_stock(
    id,
    product,
    db

):
    product_db = db.get(Product,id)
    if not product_db:
        raise HTTPException(status_code=404,detail="Product not found")
    
    product_db.stock+=product.stock
    db.commit()
    db.refresh(product_db)

    return product_db

def delete_product(
    id,
    db
):
    product_db = db.get(Product,id)
    if not product_db:
        raise HTTPException(status_code=404,detail="Product not found")
    
    db.delete(product_db)
    db.commit()

    
    return {
        "message" : "Deleted successfully"
    }
    


