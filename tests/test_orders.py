from db.models import Order
def test_create_order_success(client,user_token,db):
    response = client.post(
        "/orders",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    order = db.query(Order).filter_by(id=data["id"]).first()
    assert order is not None
    assert response.status_code == 200
    assert data["user_id"] == order.user_id
    assert data["status"] == order.status

def test_create_order_invalid_token(client):
    response = client.post(
        "/orders",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_create_order_without_token(client):
    response = client.post(
        "/orders"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_update_order_success(client,admin_token,test_order,db):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status" : "delivered"
        }
    )
    data = response.json()
    db.expire_all()
    order = db.query(Order).filter_by(id=test_order.id).first()
    assert response.status_code == 200
    assert order is not None
    assert data["user_id"] == order.user_id
    assert data["status"] == order.status

def test_update_order_not_found(client,admin_token,test_order):
    response = client.put(
        f"/admin/orders/{test_order.id + 1000}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status" : "delivered"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Order not found"

def test_update_order_invalid_token(client,test_order):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        },
        json={
            "status" : "delivered"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_update_order_without_token(client,test_order):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        json={
            "status" : "delivered"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_update_order_access_denied(client,test_order,user_token):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "status" : "delivered"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_update_order_invalid_status(client,test_order,admin_token):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status" : "invaild_status"
        }
    )
    assert response.status_code == 422

def test_update_order_empty_status(client,test_order,admin_token):
    response = client.put(
        f"/admin/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status" : ""
        }
    )
    assert response.status_code == 422


def test_delete_order_success(client,db,test_order,user_token):
    response = client.delete(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    order = db.query(Order).filter_by(id=test_order.id).first()
    assert response.status_code == 200
    assert order is None
    assert data["message"] == "Order deleted successfully"

def test_delete_order_not_found(client,test_order,user_token):
    response = client.delete(
        f"/orders/{test_order.id + 1000}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Order not found"

def test_delete_order_without_token(client,test_order):
    response = client.delete(
        f"/orders/{test_order.id}"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_delete_order_invalid_token(client,test_order):
    response = client.delete(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_delete_order_access_denied(client,test_order,admin_token):
    response = client.delete(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

