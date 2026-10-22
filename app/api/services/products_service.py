from app.db.models import Product
from app.exceptions.errors import ProductNotFound
from app.core.redis import redis_client

import logging

from fastapi import HTTPException

import json

logger = logging.getLogger(__name__)

def create_product(
    product,
    db,
    current_admin
    
):
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )
    duplicate_product = db.query(Product).filter_by(name=product.name).first()

    if duplicate_product:
        logger.warning(
            "This product is in stock",
            extra={
                "product_id" : new_product.id,
                "admin_id" : current_admin.id,
                "product_name" : product.name
            }
        )
        raise HTTPException(status_code=409,detail="Product already exists")
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        redis_client.delete("products")
        logger.info(
            "Added Product",
            extra={
                "product_id" : new_product.id,
                "product_name" : product.name,
                "product_price" : product.price,
                "product_stock" : product.stock,
                "admin_id" : current_admin.id
            }
        
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Product failed to added",
            extra={
                "admin_id" : current_admin.id,
                "product_id" : new_product.id
            }
        )

    return new_product

def get_products(
    db
):
    cached_product = redis_client.get("products")
    if cached_product:
        return json.loads(cached_product)
    
    products = db.query(Product).all()

    result = []

    for product in products:

        result.append(
            {
                "id" : product.id,
                "name" : product.name,
                "price" : product.price,
                "stock" : product.stock
            }
        )

    redis_client.set(
        "products",
        json.dumps(result),
        ex=600
    )

    return result

def update_stock(
    id,
    product,
    db,
    current_admin

):
    product_db = db.get(Product,id)

    if not product_db:
        logger.error(
            "Product not found",
            extra={
                "admin_id" : current_admin.id,
                "product_id" : id
            }
        )
        raise ProductNotFound()
    
    product_db.stock+=product.stock
    try:
        db.commit()
        db.refresh(product_db)
        redis_client.delete("products")
        logger.info(
            "Product change stock",
            extra={
                "product_id" : id,
                "added_quantity" : product.stock,
                "product_stock" : product_db.stock,
                "admin_id" : current_admin.id
            }
        )
    
    except Exception:
        db.rollback()
        logger.exception(
            "Product change stock failed",
            extra={
                "admin_id" : current_admin.id,
                "product_id" : id
            }
        )
        raise
    return product_db

def delete_product(
    id,
    db,
    current_admin
):
    product_db = db.get(Product,id)
    if not product_db:
        logger.error(
            "Product not found",
            extra={
                "admin_id" : current_admin.id,
                "product_id" : id
            }
        )
        raise ProductNotFound()
    try:
        db.delete(product_db)
        db.commit()
        redis_client.delete("products")
        logger.info(
            "Product deleted",
            extra={
                "product_id" : id,
                "admin_id" : current_admin.id
            }
        )
    except Exception:
        db.rollback()
        logger.exception(
            "Product failed delete",
            extra={
                "admin_id" : current_admin.id,
                "product_id" : id
            }
        )
        raise
    
    return {
        "message" : "Deleted successfully"
    }
    


