from fastapi import Request
from fastapi.responses import JSONResponse
from .errors import (
    ProductNotFound,
    OrderNotFound,
    InsufficientStock,
    UserNotFound,
    AccessDenied
)
async def product_not_found_handler(
    request : Request,
    exc : ProductNotFound
):
    return JSONResponse(
        status_code=404,
        content={
            "detail" : "Product not found"
        }
    )

async def order_not_found_handler(
    request : Request,
    exc : OrderNotFound
):
    return JSONResponse(
        status_code=404,
        content={
            "detail" : "Order not found"
        }
    )

async def insufficient_stock_handler(
    request : Request,
    exc : InsufficientStock
):
    return JSONResponse(
        status_code=409,
        content={
            "detail" : "Insufficient stock"
        }
    )

async def user_not_found_handler(
    request : Request,
    exc : UserNotFound
):
    return JSONResponse(
        status_code=409,
        content={
            "detail" : "User not found"
        }
    )

async def access_denied_handler(
    request : Request,
    exc : AccessDenied
):
    return JSONResponse(
        status_code=403,
        content={
            "detail" : "Access denied"
        }
    )