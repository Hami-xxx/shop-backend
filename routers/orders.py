from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Order, OrderItem, Product
from schemas import UpdateStatus, OrderItems
from dependecies import get_db
from auth import get_current_user, get_current_admin

router= APIRouter()

@router.post("/orders")
def create_order(
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    order = Order(
        user_id=current_user.id
    ) 

    db.add(order)
    db.commit()
    db.refresh()

    return order
@router.post("/orders/{id}/items")
def order_item(
    id : int,
    item : OrderItems,
    db : Session=Depends(get_db)
):
    order_db = db.get(Order,id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = OrderItem(
        order_id=order_db.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    product_db = db.get(Product,item.product_id)

    if not product_db:
        raise HTTPException(status_code=404,detail="Product not found") 

    if item.quantity > product_db.stock:
        raise HTTPException(
            status_code=409,
            detail=f"Only {product_db.stock} item are available in stock")
    
    product_db.stock -= item.quantity

    db.add(order)
    db.commit()
    db.refresh(order)
    db.refresh(product_db)

    return order

@router.put("/orders/{id}")
def update_status(
    id : int,
    order : UpdateStatus,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    order_db = db.get(Order,id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_db.status=order.status

    db.commit()
    db.refresh(order_db)

    return order_db

@router.delete("/orders/{id}/items/{item_id}")
def delete_item(
    id : int,
    item_id : int,
    db : Session=Depends(get_db)
):
    order_db = db.get(Order,id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    item_db = db.query(OrderItem).filter_by(
        id=item_id,
        order_id=order_db.id
        ).first()
    
    if not item_db:
         raise HTTPException(
            status_code=404,
            detail="Item not found in this order"
            )

    db.delete(item_db)
    db.commit()
    
    return {
        "messeage" : "Item deleted successfully"
    }   