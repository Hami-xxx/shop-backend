from models import Order, OrderItem, Product
from exceptions.errors import ProductNotFound, OrderNotFound, InsufficientStock, AccessDenied
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

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
        logger.info(
        "Order Created",
        extra={
            "user_id" : current_user.id
        }
    )


    except Exception:
        db.rollback()
        logger.exception(
        "failed to create order",
        extra={
            "user_id" : current_user.id
        }
        )
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
        logger.error(
            "Order not found",
            extra={
                "order_id" : id
            }
        )
        raise OrderNotFound()
    
    if order_db.user_id != current_user.id:
        logger.warning(
            "Access denied",
            extra={
                "user_id" : current_user.id
            }
        )
        raise AccessDenied()
    
    order = OrderItem(
        order_id=order_db.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    product_db = db.query(Product).with_for_update().filter_by(id=item.product_id).first()

    if not product_db:
        logger.error(
            "Product not found",
            extra={
                "product_id" : item.product_id
            }
        )
        raise ProductNotFound()

    if item.quantity > product_db.stock:
        logger.warning(
            "InsufficientStock",
            extra={
                "in_stock" : product_db.stock,
                "quantity" : item.quantity
            }
        )
        raise InsufficientStock()
    
    product_db.stock -= item.quantity
    try:
        db.add(order)
        db.commit()
        db.refresh(order)
        db.refresh(product_db)
        logger.info(
        "Inventory Updated successfuly",
        extra={
            "product_id" : item.product_id,
            "quantity_sold" : item.quantity,
            "remaining_stock" : product_db.stock
        }
    )
        logger.info(
        "Product added to order",
        extra={
            "product_id" : item.quantity,
            "quantity" : item.quantity,
            "order_id" : order_db.id
        }
    )

    except Exception:
        db.rollback()
        logger.exception(
        "Product added failed",
        extra={
            "product_id" : item.product_id,
            "order_id" : order_db.id
        }
        )
        raise
    
    return order

def update_status(
    id,
    order,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        logger.error(
            "Order not found",
            extra={
                "order_id" : id
            }
        )
        raise OrderNotFound()
    
    order_db.status=order.status
    try:
        db.commit()
        db.refresh(order_db)
        logger.info(
            "Order change status",
            extra={
                "order_id" : id,
                "order_status" : order.status
            }
        )
    
    except Exception:
        db.rollback()
        logger.exception(
            "Order failed change status",
            extra={
                "order_id" : id
            }
        )
        raise
    
    return order_db

def delete_order(
    id,
    current_user,
    db
):
    order_db = db.get(Order,id)
    if not order_db:
        logger.error(
            "Order not found",
            extra={
                "order_id" : id
            }
        )
        raise OrderNotFound()
    
    if order_db.user_id != current_user.id:
        logger.warning(
            "Access denied",
            extra={
                "user_id" : current_user.id
            }
        )
        raise AccessDenied()   
     
    try:
        db.delete(order_db)
        db.commit()
        logger.info(
        "User deleted order",
        extra={
            "user_id" : current_user.id,
            "order_id" : id
        }
    )
    
    except Exception:
        db.rollback()
        logger.exception(
        "User failed to deleted order",
        extra={
            "user_id" : current_user.id,
            "order_id" : id
        }
    )
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
        logger.error(
            "Order not found",
            extra={
                "order_id" : id
            }
        )
        raise OrderNotFound()
    
    if order_db.user_id != current_user.id:
        logger.warning(
            "Access denied",
            extra={
                "user_id" : current_user.id
            }
        )
        raise AccessDenied()
    
    item_db = db.query(OrderItem).filter_by(
        id=item_id,
        order_id=order_db.id
        ).first()
    
    if not item_db:
        logger.error(
            "item not found in this order",
            extra={
                "item_id" : item_id,
                "order_id" : id
            }
        )
        raise HTTPException(
            status_code=404,
            detail="Item not found in this order"
            )
    product_db = db.get(Product, item_db.product_id)
    product_db.stock += item_db.quantity
    
    try:
        db.delete(item_db)
        db.commit()
        logger.info(
        "User deleted item",
        extra={
            "user_id" : current_user.id,
            "order_id" : id,
            "item_id" : item_id
        }
    )

    
    except Exception:
        logger.exception(
            "User failed to deleted item",
        extra={
            "user_id" : current_user.id,
            "order_id" : id,
            "item_id" : item_id
        }
    )
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
        logger.error(
            "Order not found",
            extra={
                "order_id" : id
            }
        )
        raise OrderNotFound()
    
    if order_db.user_id != current_user.id:
        logger.warning(
        "Access denied",
        extra={
                "user_id" : current_user.id
            }
        )
        raise AccessDenied()
    return order_db