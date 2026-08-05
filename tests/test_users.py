from db.models import User
from tests.factories import create_test_user

def test_create_user_success(client,db):
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "12345678",
            "role" : "user"
        }
    )
    data = response.json()
    user = db.query(User).filter_by(id=data["id"]).first()
    assert response.status_code == 200
    assert user is not None
    assert user.username == "hamid"
    assert user.email == "hamid@test.com"

    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["role"] == user.role
    assert "password" not in data

def test_create_user_empty_username(client):
    response = client.post(
        "/users",
        json={
            "username" : "",
            "email" : "hamid@test.com",
            "password" : "12345678",
            "role" : "user"
        }
    )
    assert response.status_code == 422

def test_create_user_empty_password(client):
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "",
            "role" : "user"
        }
    )
    assert response.status_code == 422

def test_create_user_invalid_role(client):
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "12345678",
            "role" : "invalid_role"
        }
    )
    assert response.status_code == 422

def test_create_user_password_too_short(client):
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "1234",
            "role" : "user"
        }
    )
    assert response.status_code == 422

def test_create_user_duplicate_username(client,db):
    create_test_user(db,username="hamid")
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "12345678",
            "role" : "user"
        }
    )
    assert response.status_code == 409

def test_create_user_duplicate_email(client,db):
    create_test_user(db,email="hamid@test.com")
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "12345678",
            "role" : "user"
        }
    )
    assert response.status_code == 409

def test_create_user_duplicate_email(client,db):
    create_test_user(db,username="hamid",email="hamid@test.com")
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid@test.com",
            "password" : "12345678"
        }
    )
    assert response.status_code == 422
    users = db.query(User).filter_by(email="hamid@test.com").all()
    assert len(users) == 1
    assert users[0].email == "hamid@test.com"

def test_create_user_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "username" : "hamid",
            "email" : "hamid_gmail",
            "password" : "12345678"
        }
    )
    assert response.status_code == 422

def test_get_users_success(client,admin_token,test_admin):
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1

    user = next((u for u in data if u["id"] == test_admin.id),
    None
    )

    assert user is not None    
    assert "password" not in user
    assert user["username"] == test_admin.username
    assert user["email"] == test_admin.email
    assert user["role"] == test_admin.role

def test_get_users_without_token(client):
    response = client.get(
        "/admin/users"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_get_users_invalid_token(client):
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_get_users_access_denied(client,user_token):
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_update_users_success(client,user_token,db,test_user):
    response = client.put(
        f"/users/{test_user.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "username" : "mmdjavad",
            "email" : "mmdjavad@test.com"
        }
    )
    data = response.json()
    db.expire_all()
    user = db.query(User).filter_by(id=test_user.id).first()
    assert response.status_code == 200
    assert user is not None
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["role"] == user.role
    assert "password" not in data

def test_update_user_invalid_email(client,test_user,user_token):
    response = client.put(
        f"/users/{test_user.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "username" : "mmdjavad",
            "email" : "mmdjavad_gmail"
        }
    )
    assert response.status_code == 422

def test_update_users_without_token(client,test_user):
    response = client.put(
        f"/users/{test_user.id}",
        json={
            "username" : "mmdjavad",
            "email" : "mmdjavad@test.com"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_update_users_invalid_token(client,test_user):
    response = client.put(
        f"/users/{test_user.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        },
        json={
            "username" : "mmdjavad",
            "email" : "mmdjavad@test.com"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_update_users_not_found(client, user_token,test_user):
    response = client.put(
        f"/users/{test_user.id + 1000}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "username" : "mmdjavad",
            "email" : "mmdjavad@test.com"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"

def test_delete_users_success(client,admin_token,db,test_admin):
    response = client.delete(
        f"/users/{test_admin.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    user = db.query(User).filter_by(id=test_admin.id).first()
    assert response.status_code == 200
    assert user is None
    assert data["message"] == "Deleted successfully"

def test_delete_users_without_token(client,test_admin):
    response = client.delete(
        f"/users/{test_admin.id}"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_delete_users_invalid_token(client,test_admin):
    response = client.delete(
        f"/users/{test_admin.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"


def test_delete_users_access_denied(client,test_user, user_token):
    response = client.delete(
        f"/users/{test_user.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_delete_users_not_found(client, admin_token, test_admin):
    response = client.delete(
        f"/users/{test_admin.id + 1000}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "User not found"

def test_get_profile(client,user_token,test_user):
    response = client.get(
        "/me",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
    assert "password" not in data

def test_get_profile_without_token(client):
    response = client.get(
        "/me",
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_get_profile_invalid_token(client):
    response = client.get(
        "/me",
        headers={
            "Authorization": "Bearer abcdefgh"
                }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"