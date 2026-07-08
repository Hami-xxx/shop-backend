from fastapi import Request
from fastapi.responses import JSONResponse
from errors import ProductNotFound, OrderNotFound, InsufficientStock

async def product_not_found_handler(
    request : Request,
    exc : ProductNotFound
):
    raise JSONResponse(
        status_code=404,
        content={
            "detail" : "Product not found"
        }
    )

async def order_not_found_handler(
    request : Request,
    exc : OrderNotFound
):
    raise JSONResponse(
        status_code=404,
        content={
            "detail" : "Order not found"
        }
    )

async def insufficient_stock_handler(
    request : Request,
    exc : ProductNotFound
):
    raise JSONResponse(
        status_code=409,
        content={
            "detail" : "Insufficient stock"
        }
    )