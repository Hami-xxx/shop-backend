from fastapi import FastAPI
from database import Base, engine
from routers import users, products, orders

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)