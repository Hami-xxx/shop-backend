from tests.factories import create_test_user
from core.auth import hash_refresh_token
from db.models import User
def test_login_success(client,db):
    create_test_user(db,username="hamid",password="12345678")
    response = client.post(
        "/login",
        json={
            "username" : "hamid",
            "password" : "12345678"
        }
    )
    data = response.json()
    user = db.query(User).filter_by(username="hamid").first()
    assert response.status_code == 200
    assert "password" not in data
    assert "access_token" in data
    assert "refresh_token" in data

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20

    assert len(user.refresh_token) == 1
    assert isinstance(data["refresh_token"], str)
    assert len(data["refresh_token"]) >= 40

def test_login_invalid_username(client,db):
    create_test_user(db,username="mmdjavad")
    response= client.post(
        "/login",
        json={
            "username" : "hamid",
            "password" : "12345678"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid username or password"

def test_login_invalid_password(client,db):
    create_test_user(db,username="hamid")
    response= client.post(
        "/login",
        json={
            "username" : "hamid",
            "password" : "12345678910"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid username or password"

def test_login_create_refresh_token(client,db):
    create_test_user(db,username="hamid")
    response= client.post(
            "/login",
            json={
                "username" : "hamid",
                "password" : "12345678"
            }
        )
    data = response.json()
    user = db.query(User).filter_by(username="hamid").first()
    assert response.status_code == 200
    assert isinstance(data["refresh_token"], str)
    assert len(data["refresh_token"]) >= 40
    assert len(user.refresh_token) == 1
    assert user.refresh_token[0].token_hash == hash_refresh_token(data["refresh_token"])

def test_login_empty_username(client,db):
    create_test_user(db)
    response= client.post(
            "/login",
            json={
                "username" : "",
                "password" : "12345678"
            }
        )
    assert response.status_code == 422

def test_login_empty_password(client,db):
    create_test_user(db,username="hamid")
    response = client.post(
        "/login",
        json={
            "username" : "hamid",
            "password" : ""
        }
    )
    assert response.status_code == 422

def test_login_missing_username(client,db):
    create_test_user(db)
    response = client.post(
        "/login",
        json={
            "password": "12345678"
        }
    )
    assert response.status_code == 422

def test_login_missing_password(client,db):
    create_test_user(db,username="hamid")
    response = client.post(
        "/login",
        json={
            "username": "hamid"
        }
    )
    assert response.status_code == 422