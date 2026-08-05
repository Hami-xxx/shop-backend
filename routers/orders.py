from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import order_service
from schemas import UpdateStatus, OrderItems, OrderRespone
from core.dependecies import get_db
from core.auth import get_current_user, get_current_admin

router= APIRouter()

@router.post("/orders",summary="Create Order",description="Create order with current user")
def create_order(
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.create_order(
        current_user=current_user,
        db=db
    )

@router.post("/orders/{id}/items",summary="Add item to order")
def order_item(
    id : int,
    item : OrderItems,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.order_item(
        id=id,
        item=item,
        current_user=current_user,
        db=db
    )

@router.put("/admin/orders/{id}",summary="Change order status",description="Only admin can update status")
def update_status(
    id : int,
    order : UpdateStatus,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return order_service.update_status(
        id=id,
        order=order,
        db=db,
        current_admin=current_admin
    )

@router.delete("/orders/{id}",summary="Delete order")
def delete_order(
    id : int,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.delete_order(
        id=id,
        current_user=current_user,
        db=db
    )

@router.delete("/orders/{id}/items/{item_id}",summary="Delete item in order")
def delete_item(
    id : int,
    item_id : int,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.delete_item(
        id=id,
        item_id=item_id,
        current_user=current_user,
        db=db
    )

@router.get("/orders/{id}", response_model=OrderRespone,summary="Get order")
def get_order(
    id : int,
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.get_order(
        id=id,
        current_user=current_user,
        db=db
    )