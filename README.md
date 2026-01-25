# 📊 E-commerce REST API

A production-ready REST API for e-commerce applications built with FastAPI and PostgreSQL. Features JWT authentication, full CRUD operations, and auto-generated Swagger documentation.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- **JWT Authentication** - Secure user registration and login
- **Full CRUD Operations** - Create, Read, Update, Delete for products
- **Search & Filter** - Filter products by category, price range
- **Pagination** - Efficient data loading with offset/limit
- **Auto Documentation** - Swagger UI and ReDoc out of the box
- **Database Migrations** - Alembic for schema management
- **Input Validation** - Pydantic schemas for data validation

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Web Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| JWT | Authentication |
| Alembic | Migrations |

## 📁 Project Structure

```
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── product.py       # Product model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User Pydantic schemas
│   │   └── product.py       # Product Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   └── products.py      # Product CRUD endpoints
│   └── utils/
│       ├── __init__.py
│       └── security.py      # Password hashing, JWT
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/EhtishamProAI/ecommerce-api.git
cd ecommerce-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your database credentials

# Run the server
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user info |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/products` | Create new product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| GET | `/products/search` | Search products |

## 👨‍💻 Author

**Ehtisham Ashraf**  
Senior AI Software Engineer | Full-Stack Developer

- GitHub: [@EhtishamProAI](https://github.com/EhtishamProAI)
- Email: kingehtsham0@gmail.com
