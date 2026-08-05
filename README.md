# 🛒 Backend Shop

A production-ready E-commerce REST API built with **FastAPI**.

This project demonstrates modern backend development practices including authentication, authorization, caching, database migrations, automated testing, and containerization.

---

# ✨ Features

## Authentication

* JWT Authentication
* Access Token
* Refresh Token Rotation
* Secure Password Hashing (bcrypt)
* Logout
* Token Validation

---

## Authorization

Role Based Access Control (RBAC)

### Admin

* Manage Products
* Update Order Status
* View Users

### User

* Browse Products
* Create Orders
* Manage Order Items

---

## Product Management

* Create Product
* Update Product
* Delete Product
* Product Listing
* Product Inventory Management

---

## Order Management

* Create Orders
* Add Order Items
* Update Order Status

Supported order statuses:

* Pending
* Paid
* Sending
* Delivered

---

## Redis Cache

Redis is used for performance optimization.

Current implementation:

* Product list caching
* Cache invalidation after product updates
* Cache invalidation after product deletion

---

## Logging

Application logging includes:

* Successful operations
* Failed operations
* Security events
* Error tracking

---

# 🛠 Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic

### Database

* PostgreSQL

### Database Migration

* Alembic

### Cache

* Redis

### Testing

* Pytest
* Pytest Coverage

### Deployment

* Docker
* Docker Compose

---

# 📁 Project Structure

```text
Backend_Shop/
│
├── alembic/
│
├── core/
│
├── db/
│
├── exceptions/
│
├── routers/
│
├── services/
│
├── tests/
│
└── main.py
```

---

# 🔐 Authentication Flow

1. User Login
2. Generate Access Token
3. Generate Refresh Token
4. Refresh Token Rotation
5. Logout

---

# 📚 API Documentation

Swagger UI

```
/docs
```

ReDoc

```
/redoc
```

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/Hami-xxx/shop-backend.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Variables

Create a `.env` file using `.env.example`

Example variables:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REDIS_HOST=
REDIS_PORT=
```

---

# 🐳 Run with Docker

```bash
Services

- FastAPI
- PostgreSQL
- Redis
docker compose up --build
```

---

# 🧪 Running Tests

Run all tests

```bash
pytest
```

Run tests with coverage

```bash
pytest --cov=. --cov-report=term-missing
```

Current test coverage:

**≈95%**

---

# 🔒 Security Features

* Password Hashing (bcrypt)
* JWT Authentication
* Refresh Token Hashing
* Role-Based Authorization
* Input Validation
* Protected Admin Routes

---

# 📌 Main Endpoints

## Authentication

* POST `/login`
* POST `/refresh`
* POST `/logout`

## Users

* POST `/users`
* GET `/users`
* PUT `/`users/{id}
* DELETE /users/{id}
* GET /me

## Products

* GET `/products`
* POST `/admin/products`
* PUT `/admin/products/{id}`
* DELETE `/admin/products/{id}`

## Orders

* POST `/orders`
* POST `/orders/items`
* PUT `/admin/orders/{id}`
* DELETE /orders/{id}
* DELETE /orders/{id}/items/{id}
* GET /orders/{id}

---

# 📈 Future Improvements

* GitHub Actions (CI)
* Cloud Deployment
* Rate Limiting
* Monitoring & Metrics
* API Versioning

---

# 📄 License

This project is intended for educational and portfolio purposes.
