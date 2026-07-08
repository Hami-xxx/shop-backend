from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import order_service
from schemas import UpdateStatus, OrderItems, OrderRespone
from dependecies import get_db
from auth import get_current_user, get_current_admin

router= APIRouter()

@router.post("/orders")
def create_order(
    current_user=Depends(get_current_user),
    db : Session=Depends(get_db)
):
    return order_service.create_order(
        current_user=current_user,
        db=db
    )

@router.post("/orders/{id}/items")
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

@router.put("/admin/orders/{id}")
def update_status(
    id : int,
    order : UpdateStatus,
    db : Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return order_service.update_status(
        id=id,
        order=order,
        db=db
    )

@router.delete("/orders/{id}")
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

@router.delete("/orders/{id}/items/{item_id}")
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

@router.get("/orders/{id}", response_model=OrderRespone)
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