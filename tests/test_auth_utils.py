import pytest
from jose import jwt
from fastapi import HTTPException

from core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    create_refresh_token,
    hash_refresh_token,
    get_current_user,
    get_current_admin,
)

from core.config import settings
from tests.factories import create_test_user


def test_hash_password():
    password = "12345678"

    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)
    assert len(hashed) > 20


def test_verify_password_success():
    password = "12345678"

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_invalid_password():
    password = "12345678"

    hashed = hash_password(password)

    assert verify_password("abcdefgh", hashed) is False


def test_create_access_token():
    token = create_access_token({"sub": "1"})

    assert isinstance(token, str)
    assert len(token) > 20


def test_verify_token_success():
    token = create_access_token({"sub": "1"})

    payload = verify_token(token)

    assert payload["sub"] == "1"
    assert "exp" in payload


def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc:
        verify_token("abcdefgh")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_create_refresh_token():
    token = create_refresh_token()

    assert isinstance(token, str)
    assert len(token) >= 40


def test_create_refresh_token_unique():
    token1 = create_refresh_token()
    token2 = create_refresh_token()

    assert token1 != token2


def test_hash_refresh_token():
    token = create_refresh_token()

    token_hash = hash_refresh_token(token)

    assert isinstance(token_hash, str)
    assert len(token_hash) == 64


def test_hash_refresh_token_same_token():
    token = create_refresh_token()

    hash1 = hash_refresh_token(token)
    hash2 = hash_refresh_token(token)

    assert hash1 == hash2


def test_get_current_user_success(db):
    user = create_test_user(db)

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    current_user = get_current_user(token, db)

    assert current_user.id == user.id
    assert current_user.username == user.username


def test_get_current_user_invalid_sub(db):
    token = create_access_token(
        {
            "username": "hamid"
        }
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token, db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_get_current_user_not_found(db):
    token = create_access_token(
        {
            "sub": "999999"
        }
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token, db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_get_current_admin_success(db):
    admin = create_test_user(db, role="admin")

    result = get_current_admin(admin)

    assert result.id == admin.id
    assert result.role == "admin"


def test_get_current_admin_access_denied(db):
    user = create_test_user(db, role="user")

    with pytest.raises(HTTPException) as exc:
        get_current_admin(user)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Access denied"