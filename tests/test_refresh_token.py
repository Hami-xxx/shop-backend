from db.models import RefreshToken
from core.auth import hash_refresh_token
import uuid

def test_create_refresh_token(client,refresh_token,db):
    response = client.post(
        "/refresh",
        json={
            "token" : refresh_token
        }
    )
    data = response.json()
    token_hash = hash_refresh_token(refresh_token)
    refresh = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert refresh is None

    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20
    assert data["access_token"] != data["refresh_token"]

    assert isinstance(data["refresh_token"], str)
    assert len(data["refresh_token"]) >= 40

    new_hash = hash_refresh_token(data["refresh_token"])
    new_refresh = db.query(RefreshToken).filter_by(
    token_hash=new_hash
    ).first()
    assert new_refresh is not None

def test_invalid_refresh_token(client):
    response = client.post(
        "/refresh",
        json={
            "token" : uuid.uuid4().hex * 2
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid refresh token"

def test_expired_refresh_token(client,db,expired_refresh_token):
    response = client.post(
        "/refresh",
        json={
            "token" : expired_refresh_token
        }
    )
    data = response.json()
    token_hash = hash_refresh_token(expired_refresh_token)
    refresh = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    assert response.status_code == 401
    assert data["detail"] == "Refresh token expired"
    assert refresh is None

def test_empty_refresh_token(client):
    response = client.post(
        "/refresh",
        json={
            "token" : ""
        }
    )
    assert response.status_code == 422

def test_reuse_refresh_token(client,reuse_refresh_token):
    response = client.post(
        "/refresh",
        json={
            "token" : reuse_refresh_token
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token" 

def test_logout_success(client,db,refresh_token):
    response = client.post(
        "/logout",
        json={
            "token" : refresh_token
        }
    )
    data = response.json()
    token_hash = hash_refresh_token(refresh_token)
    refresh = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    assert response.status_code == 200
    assert data["message"] == "Logout successfully"
    assert refresh is None

def test_logout_invalid_refresh_token(client):
    response = client.post(
        "/logout",
        json={
            "token" : uuid.uuid4().hex * 2
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid refresh token"

def test_logout_expired_refresh_token(client,expired_refresh_token):
    response = client.post(
        "/logout",
        json={
            "token" : expired_refresh_token
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Refresh token expired"

def test_logout_empty_refresh_token(client):
    response = client.post(
        "/logout",
        json={
            "token" : ""
        }
    )
    assert response.status_code == 422