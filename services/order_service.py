from models import Order, OrderItem, Product
from exceptions.errors import ProductNotFound, OrderNotFound, InsufficientStock
from fastapi import HTTPException
def create_order(
    current_user,
    db
):
    order = Order(
        user_id=current_user.id
    ) 
    try:
        db.add(order)
        db.commit()
        db.refresh(order)

    except Exception:
        db.rollback()
        raise
    
    return order

def order_item(
    id,
    item,
    current_user,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        raise OrderNotFound
    
    if order_db.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")
    
    order = OrderItem(
        order_id=order_db.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    product_db = db.get(Product,item.product_id)

    if not product_db:
        raise ProductNotFound

    if item.quantity > product_db.stock:
        raise InsufficientStock
    
    product_db.stock -= item.quantity
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
        db.refresh(product_db)

    except Exception:
        db.rollback()
        raise

    return order

def update_status(
    id,
    order,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        raise OrderNotFound
    
    order_db.status=order.status
    try:
        db.commit()
        db.refresh(order_db)
    
    except Exception:
        db.rollback()
        raise
    
    return order_db

def delete_order(
    id,
    current_user,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        raise OrderNotFound
    
    if order_db.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")    
    
    try:
        db.delete(order_db)
        db.commit()
    
    except Exception:
        db.rollback()
        raise
    
    return {
        "message" : "Order deleted successfully"
    }

def delete_item(
    id,
    item_id,
    current_user,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        raise OrderNotFound
    
    if order_db.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")
    
    item_db = db.query(OrderItem).filter_by(
        id=item_id,
        order_id=order_db.id
        ).first()
    
    if not item_db:
         raise HTTPException(
            status_code=404,
            detail="Item not found in this order"
            )
    product_db = db.get(Product, item_db.product_id)
    product_db.stock += item_db.quantity
    
    try:
        db.delete(item_db)
        db.commit()
    
    except Exception:
        db.rollback()
        raise
    
    return {
        "messeage" : "Item deleted successfully"
    }

def get_order(
    id,
    current_user,
    db
):
    order_db = db.get(Order,id)

    if not order_db:
        raise OrderNotFound
    
    if order_db.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")

    return order_db