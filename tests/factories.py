from app.db.models import User, Product
from app.core.auth import hash_password
import uuid
from tests.redis import redis_client
import json

def create_test_user(
    db,
    username=None,
    email=None,
    password="12345678",
    role="admin"
):

    if username is None:
        username=f"user_{uuid.uuid4().hex}"

    if email is None:
        email=f"{uuid.uuid4().hex}@test.com"

    user = User(
        username=username,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_test_product(
    db,
    name="PC",
    price=1200,
    stock=100
):

    new_product = Product(
        name=name,
        price=price,
        stock=stock
        )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product