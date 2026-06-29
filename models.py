from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,default="user")
    orders = relationship(
        "Order",
        back_populates="user"
    )


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    stock = Column(Integer,nullable=False,default=0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id"
        )
    )
    user = relationship(
        "User",
        back_populates="orders"
    )

    status = Column(String,default="pending")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantity = Column(Integer,nullable=True)