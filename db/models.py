from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

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
    refresh_token = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    stock = Column(Integer,nullable=False,default=0)

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    user = relationship(
        "User",
        back_populates="orders"
    )
    
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    status = Column(String,default="pending")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )
    order = relationship(
        "Order",
        back_populates="items"
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )
    product = relationship(
        "Product",
        back_populates="order_items"
    )
    quantity = Column(Integer,nullable=False)

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    token_hash = Column(String,nullable=False,unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    expires_at = Column(DateTime, nullable=False)

    user = relationship(
        "User",
        back_populates="refresh_token"
    )