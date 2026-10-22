from fastapi import FastAPI
from app.api.routers import orders
from app.api.routers import products
from app.api.routers import users
from app.exceptions.errors import (
    ProductNotFound,
    OrderNotFound,
    InsufficientStock,
    UserNotFound,
    AccessDenied
)

from app.exceptions.handlers import (
    product_not_found_handler,
    order_not_found_handler,
    insufficient_stock_handler,
    user_not_found_handler,
    access_denied_handler
)

import app.core.logging_config

app = FastAPI()


app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

app.add_exception_handler(
    ProductNotFound,
    product_not_found_handler
)
app.add_exception_handler(
    OrderNotFound,
    order_not_found_handler
)
app.add_exception_handler(
    InsufficientStock,
    insufficient_stock_handler
)
app.add_exception_handler(
    UserNotFound,
    user_not_found_handler
)
app.add_exception_handler(
    AccessDenied,
    access_denied_handler
)
