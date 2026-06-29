from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Order, OrderItem, Product
from schemas import UpdateStatus, OrderItems, UpdateItems
from dependecies import get_db
from auth import get_current_user

router= APIRouter()

@router.post("/orders")
def create_order(
    db : Session=Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = Order(
        user_id=current_user.id
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order
@router.put("/orders/{id}")
def update_status(
    id : int,
    order : UpdateStatus,
    db : Session=Depends(get_db)
):
    order_db = db.get(Order,id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")

    order_db.status=order.status
    db.commit()
    db.refresh(order_db)

    return order_db
    

@router.get("/me/orders")
def my_order(
    current_user=Depends(get_current_user)
):
    return current_user.orders

@router.post("/orders/{order_id}/items")
def add_item(
    order_id : int,
    order : OrderItems,
    db : Session=Depends(get_db),
):
    order_db = db.get(Order,order_id)
    if not order_db:
        raise HTTPException(status_code=404,detail="Order not found")
    
    item = OrderItem(
        order_id=order_id,
        product_id=order.product_id,
        quantity=order.quantity
    )

    product_db = db.get(Product,order.product_id)
    product_db.stock -= order.quantity
    
    db.add(item)
    db.commit()
    db.refresh(item)
    db.refresh(product_db)

    return item, product_db

@router.get("/orders/{order_id}/items")
def get_orderitems(
    order_id : int,
    db : Session=Depends(get_db)
):
    order_db = db.get(OrderItem,order_id)
    if not order_db:
        raise HTTPException(status_code=404,detail="Order not found")
    
    products = (
        db.query(Product)
        .join(OrderItem)
        .filter(OrderItem.order_id == order_id)
        .all()
    )
    return products
