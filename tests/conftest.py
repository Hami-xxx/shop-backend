import pytest
from fastapi.testclient import TestClient
from main import app
from tests.database import override_get_db, TestSessionLocal, testing_engine
from core.dependecies import get_db
from core.auth import hash_password, hash_refresh_token, create_refresh_token
from db.models import User, RefreshToken, Order, OrderItem
from db.database import Base
from datetime import datetime, timedelta
from tests.redis import redis_client
from tests.factories import create_test_product


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def user_token(client,test_user):
    response_login = client.post(
        "/login",
        json={
            "username" : test_user.username,
            "password" : "12345678"
        }
    )
    assert response_login.status_code == 200
    return response_login.json()["access_token"]

@pytest.fixture
def admin_token(client,test_admin):
    response_login = client.post(
        "/login",
        json={
            "username" : test_admin.username,
            "password" : "12345678"
        }
    )
    assert response_login.status_code == 200
    return response_login.json()["access_token"]

@pytest.fixture
def refresh_token(client,test_user):
    response_login = client.post(
        "/login",
        json={
            "username" : test_user.username,
            "password" : "12345678"
        }
    )
    assert response_login.status_code == 200
    return response_login.json()["refresh_token"]

@pytest.fixture
def expired_refresh_token(db,test_user):
    refresh_token = create_refresh_token()
    refresh = RefreshToken(
        user_id = test_user.id,
        token_hash = hash_refresh_token(refresh_token),
        expires_at = datetime.utcnow() - timedelta(minutes=1)
    )
    db.add(refresh)
    db.commit()
    db.refresh(refresh)

    return refresh_token

@pytest.fixture
def reuse_refresh_token(client,refresh_token):
    response = client.post(
        "/refresh",
        json={
            "token" : refresh_token
        }
    )
    assert response.status_code == 200
    return refresh_token

@pytest.fixture
def db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def redis():
    redis_client.flushdb()
    return redis_client

@pytest.fixture
def test_user(db):
    user = User(
        username="hamid",
        email="hamid@test.com",
        password=hash_password("12345678")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture
def test_admin(db):
    admin = User(
        username="admin",
        email="admin@test.com",
        password=hash_password("12345678"),
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin

@pytest.fixture
def product(db):
    return create_test_product(db)

@pytest.fixture
def test_order(test_user,db):
    order = Order(
        user_id=test_user.id
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return order

@pytest.fixture
def test_item(test_order,product,db):
    item = OrderItem(
        order_id=test_order.id,
        product_id=product.id,
        quantity = 1
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=testing_engine)
    Base.metadata.create_all(bind=testing_engine)

    yield

    Base.metadata.drop_all(bind=testing_engine)
