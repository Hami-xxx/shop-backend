from db.models import Product
from tests.factories import create_test_product
import json

def test_create_product_success(client,db,redis,admin_token):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name" : "PC",
            "price" : 1200,
            "stock" : 100
        }
    )
    data = response.json()

    product = db.query(Product).filter_by(name=data["name"]).first()
    cashed = redis.get("products")
    assert response.status_code == 200
    assert product is not None
    assert data["name"] == product.name
    assert data["price"] == product.price
    assert data["stock"] == product.stock
    assert cashed is None

def test_create_duplicate_product(client,db,admin_token):
    create_test_product(db)
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name" : "PC",
            "price" : 1200,
            "stock" : 100
        }
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Product already exists"

def test_create_product_empty_name(client,admin_token):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name" : "",
            "price" : 1200,
            "stock" : 100
            }
        )
    assert response.status_code == 422

def test_create_product_zero_price(client,admin_token):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name" : "PC",
            "price" : 0,
            "stock" : 100
            }
        )
    assert response.status_code == 422

def test_create_product_zero_stock(client,admin_token):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name" : "PC",
            "price" : 1200,
            "stock" : 0
            }
        )
    assert response.status_code == 422

def test_create_product_invalid_token(client):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": "Bearer abcdefgh"
        },
        json={
            "name" : "PC",
            "price" : 1200,
            "stock" : 100
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_create_product_without_token(client):
    response = client.post(
        "/admin/products",
        json={
            "name" : "PC",
            "price" : 1200,
            "stock" : 100
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_create_product_access_denied(client,user_token):
    response = client.post(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_get_product_success(client,db,redis,user_token,product):
    response = client.get(
        "/products",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1

    product_db = next((p for p in data if p["id"] == product.id),
    None
    )

    assert product_db is not None
    assert product_db["name"] == product.name
    assert product_db["price"] == product.price
    assert product_db["stock"] == product.stock
    redis.set(
        "products",
        json.dumps(data),
        ex=600
    )
    cached = json.loads(redis.get("products"))

    assert isinstance(cached, list)
    assert any(p["id"] == product.id for p in cached)

def test_update_product_success(client,db,redis,admin_token,product):
    response = client.put(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "stock" : 10
        }
    )
    data = response.json()
    db.expire_all()
    product_db = db.query(Product).filter_by(id=product.id).first()
    cashed = redis.get("products")
    assert response.status_code == 200
    assert product_db is not None
    assert cashed is None
    assert data["id"] == product_db.id
    assert data["name"] == product_db.name
    assert data["price"] == product_db.price
    assert data["stock"] == product_db.stock

def test_update_product_not_found(client,admin_token,product):
    response = client.put(
        f"/admin/products/{product.id + 1000}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "stock" : 10
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Product not found"

def test_update_product_zero_stock(client,admin_token,product):
    response = client.put(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "stock" : 0
        }
    )
    assert response.status_code == 422

def test_update_product_invalid_token(client,product):
    response = client.put(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        },
        json={
            "stock" : 10
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_update_product_without_token(client,product):
    response = client.put(
        f"/admin/products/{product.id}",
        json={
            "stock" : 10
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_update_product_access_denied(client,user_token,product):
    response = client.put(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "stock" : 10
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"

def test_delete_product(client,db,admin_token,redis,product):
    response = client.delete(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )
    data = response.json()
    product_db = db.query(Product).filter_by(id=product.id).first()
    cashed = redis.get("products")
    assert response.status_code == 200
    assert product_db is None
    assert cashed is None
    assert data["message"] == "Deleted successfully"

def test_delete_product_not_found(client,admin_token,product):
    response = client.delete(
        f"/admin/products/{product.id + 1000}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Product not found"

def test_delete_product_invalid_token(client,product):
    response = client.delete(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": "Bearer abcdefgh"
        }
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"

def test_delete_product_without_token(client,product):
    response = client.delete(
        f"/admin/products/{product.id}"
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Not authenticated"

def test_delete_product_access_denied(client,user_token,product):
    response = client.delete(
        f"/admin/products/{product.id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Access denied"
