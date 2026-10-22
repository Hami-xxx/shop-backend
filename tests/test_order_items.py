from app.db.models import OrderItem, Product

def test_create_item_success(client,db,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : product.id,
            "quantity" : 1
        }
    )
    data = response.json()
    db.expire_all()
    item = db.query(OrderItem).filter_by(id=data["id"]).first()
    product_db = db.query(Product).filter_by(id=product.id).first()
    assert response.status_code == 200
    assert item is not None
    assert product_db is not None
    assert data["order_id"] == item.id
    assert data["product_id"] == item.product_id
    assert data["quantity"] == item.quantity
    assert  product.stock == product_db.stock

def test_create_item_order_not_found(client,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id + 1000}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : product.id,
            "quantity" : 1
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Order not found"

def test_create_item_product_not_found(client,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : product.id + 1000,
            "quantity" : 1
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Product not found"

def test_create_item_Insufficient_stock(client,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : product.id,
            "quantity" : product.stock + 1000
        }
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Insufficient stock"

def test_create_item_invalid_product_id(client,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : -1,
            "quantity" : 1
        }
    )
    assert response.status_code == 422


def test_create_item_invalid_quantity(client,test_order,user_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id" : 1,
            "quantity" : -1
        }
    )
    assert response.status_code == 422

def test_create_item_without_token(client,test_order,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        json={
            "product_id" : product.id,
            "quantity" : product.stock
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_create_item_invalid_token(client,test_order,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": "Bearer abcdefgh"
        },
        json={
            "product_id" : product.id,
            "quantity" : product.stock
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_create_item_access_denied(client,test_order,admin_token,product):
    response = client.post(
        f"/orders/{test_order.id}/items",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "product_id" : product.id,
            "quantity" : product.stock
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_delete_item_success(client,db,test_order,user_token,product,test_item):
    response = client.delete(
        f"/orders/{test_order.id}/items/{test_item.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    item = db.query(OrderItem).filter_by(id=test_item.id).first()
    product_db = db.query(Product).filter_by(id=product.id).first()
    assert response.status_code == 200
    assert item is None
    assert product_db is not None
    assert data["message"] == "Item deleted successfully"
    assert product.stock == product_db.stock

def test_delete_item_order_not_found(client,test_order,user_token,test_item):
    response = client.delete(
        f"/orders/{test_order.id + 1000}/items/{test_item.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Order not found"

def test_delete_item_not_found(client,test_order,user_token,test_item):
    response = client.delete(
        f"/orders/{test_order.id}/items/{test_item.id + 1000}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Item not found in this order"

def test_delete_item_without_token(client,test_order,test_item):
    response = client.delete(
        f"/orders/{test_order.id}/items/{test_item.id}"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_delete_item_inavlid_token(client,test_order,test_item):
    response = client.delete(
        f"/orders/{test_order.id}/items/{test_item.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_delete_item_access_denied(client,test_order,admin_token,test_item):
    response = client.delete(
        f"/orders/{test_order.id}/items/{test_item.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_get_order_success(client,test_order,user_token):
    response = client.get(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_order.id
    assert isinstance(data["user"], dict)
    assert isinstance(data["items"], list)
    assert len(data) >= 1
    assert data["status"] == test_order.status

def test_get_order_not_found(client,test_order,user_token):
    response = client.get(
        f"/orders/{test_order.id + 1000}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Order not found"

def test_get_order_without_token(client,test_order):
    response = client.get(
        f"/orders/{test_order.id}"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_get_order_invalid_token(client,test_order):
    response = client.get(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_get_order_invalid_token(client,test_order,admin_token):
    response = client.get(
        f"/orders/{test_order.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"
