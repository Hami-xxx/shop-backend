from fastapi import FastAPI
from database import Base, engine
from routers import users, products, orders
from exceptions.errors import (
    ProductNotFound,
    OrderNotFound,
    InsufficientStock,
)

from exceptions.handlers import (
    product_not_found_handler,
    order_not_found_handler,
    insufficient_stock_handler,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

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