# fastinit - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Project Initialization](#project-initialization)
4. [Component Generation](#component-generation)
5. [Configuration](#configuration)
6. [JWT Authentication](#jwt-authentication)
7. [Database Setup](#database-setup)
8. [Docker Deployment](#docker-deployment)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Installation

### From Source

```bash
git clone <repository-url>
cd fastapi-starter
pip install -e .
```

### Using Installation Scripts

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Unix/Mac (Bash):**
```bash
chmod +x install.sh
./install.sh
```

### Verify Installation

```bash
fastinit version
```

---

## Basic Usage

### Create Your First Project

```bash
# Simple project
fastinit init my-first-api

# Navigate to project
cd my-first-api

# Set up virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Unix/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for interactive API documentation.

---

## Project Initialization

### Command Syntax

```bash
fastinit init <project-name> [OPTIONS]
```

### Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `--output, -o` | Output directory | `--output ./projects` |
| `--db` | Include database support | `--db` |
| `--db-type` | Database type | `--db-type postgresql` |
| `--jwt` | Include JWT authentication | `--jwt` |
| `--logging` | Include logging configuration | `--logging` |
| `--docker` | Include Docker configuration | `--docker` |
| `--python-version` | Python version | `--python-version 3.11` |
| `--interactive, -i` | Interactive mode | `--interactive` |
| `--force, -f` | Overwrite existing directory | `--force` |

### Examples

#### 1. Basic Project
```bash
fastinit init my-api
```

#### 2. Project with PostgreSQL
```bash
fastinit init my-api --db --db-type postgresql
```

#### 3. Project with JWT Auth
```bash
fastinit init my-api --jwt --logging
```

#### 4. Full-Featured Project
```bash
fastinit init my-api \
  --db --db-type postgresql \
  --jwt \
  --logging \
  --docker \
  --python-version 3.11
```

#### 5. Interactive Mode
```bash
fastinit init my-api --interactive
```

The CLI will prompt you for each option.

---

## Component Generation

### Generate a Model

Create a SQLAlchemy model:

```bash
fastinit new model User --fields "name:str,email:str,age:int,is_active:bool"
```

**Supported field types:**
- `str`, `string` → String(255)
- `int`, `integer` → Integer
- `float`, `decimal` → Float
- `bool`, `boolean` → Boolean
- `text` → Text
- `datetime` → DateTime

**Generated file:** `app/models/user.py`

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Generate Pydantic Schemas

Create Pydantic schemas for request/response validation:

```bash
fastinit new schema User --fields "name:str,email:str,age:int,is_active:bool"
```

**Generated file:** `app/schemas/user.py`

The schema includes:
- `UserBase` - Base schema with common fields
- `UserCreate` - Schema for creating users (all fields required)
- `UserUpdate` - Schema for updating users (all fields optional)
- `UserResponse` - Schema for API responses (includes id, timestamps)

```python
class UserBase(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
```

**Benefits:**
- Type-safe request/response validation
- Automatic OpenAPI schema generation
- Separation of database models from API contracts
- FastAPI automatic serialization with `response_model`

### Generate a Service

Create a service class with CRUD operations:

```bash
fastinit new service UserService --model User
```

**Generated file:** `app/services/user_service.py`

The service includes:
- `get_all(db, skip, limit)` - Get all records
- `get_by_id(db, id)` - Get by ID
- `create(db, **kwargs)` - Create new record
- `update(db, id, **kwargs)` - Update record
- `delete(db, id)` - Delete record

### Generate a Route

Create API endpoints:

```bash
fastinit new route users --service UserService
```

**Generated file:** `app/api/routes/users.py`

The route includes REST endpoints with Pydantic schema validation:
- `GET /users` - List all (returns `List[UserResponse]`)
- `GET /users/{id}` - Get by ID (returns `UserResponse`)
- `POST /users` - Create (accepts `UserCreate`, returns `UserResponse`)
- `PUT /users/{id}` - Update (accepts `UserUpdate`, returns `UserResponse`)
- `DELETE /users/{id}` - Delete (returns 204 No Content)

**Example endpoint:**
```python
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    return UserService.create(db, **data.model_dump())
```

Note: FastAPI automatically converts SQLAlchemy models to Pydantic schemas using `response_model` and `from_attributes=True`.

### Generate Complete CRUD

Create model, schema, service, and routes in one command:

```bash
fastinit new crud Product --fields "name:str,price:float,description:text,in_stock:bool"
```

This generates:
- `app/models/product.py` - SQLAlchemy database model
- `app/schemas/product.py` - Pydantic schemas (Create, Update, Response)
- `app/services/product_service.py` - Business logic layer
- `app/api/routes/products.py` - REST API endpoints

**Complete workflow:**
1. Request hits endpoint with JSON data
2. FastAPI validates against Pydantic schema (`ProductCreate`)
3. Service layer processes business logic
4. SQLAlchemy model interacts with database
5. FastAPI serializes response using `ProductResponse` schema

---

## Configuration

### Environment Variables

All projects use `.env` file for configuration. Copy the example:

```bash
cp .env.example .env
```

### Basic Configuration

```env
# Project
PROJECT_NAME=my-api
VERSION=0.1.0
DESCRIPTION=My FastAPI Application

# API
API_V1_STR=/api/v1

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Database Configuration

```env
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql://username:password@localhost:3306/dbname

# SQLite
DATABASE_URL=sqlite:///./app.db
```

### Logging Configuration

```env
LOG_LEVEL=INFO
```

---

## JWT Authentication

### Basic Setup

When you create a project with `--jwt`:

```bash
fastinit init my-api --jwt
```

### Configuration

```env
# JWT Settings
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Creating Tokens

```python
from app.core.security import create_access_token
from datetime import timedelta

# Create token
token_data = {"sub": "user@example.com", "role": "admin"}
token = create_access_token(token_data)

# Create token with custom expiration
token = create_access_token(
    token_data,
    expires_delta=timedelta(hours=24)
)
```

### Protecting Endpoints

```python
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {
        "message": "This is a protected endpoint",
        "user": current_user
    }
```

### Using JWKS (Remote Key Verification)

Configure in `.env`:

```env
USE_JWKS=true
JWKS_URL=https://your-auth-provider.com/.well-known/jwks.json
ISSUER=https://your-auth-provider.com
AUDIENCE=your-api-identifier
```

Common providers:
- **Auth0:** `https://<your-domain>.auth0.com/.well-known/jwks.json`
- **Okta:** `https://<your-domain>.okta.com/oauth2/default/v1/keys`
- **Azure AD:** `https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys`

---

## Database Setup

### PostgreSQL Setup

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE my_api_db;
CREATE USER my_api_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE my_api_db TO my_api_user;
```

3. Configure `.env`:
```env
DATABASE_URL=postgresql://my_api_user:password@localhost:5432/my_api_db
```

### MySQL Setup

1. Install MySQL
2. Create database:
```sql
CREATE DATABASE my_api_db;
CREATE USER 'my_api_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON my_api_db.* TO 'my_api_user'@'localhost';
```

3. Configure `.env`:
```env
DATABASE_URL=mysql://my_api_user:password@localhost:3306/my_api_db
```

### SQLite Setup

No installation required! Just configure:

```env
DATABASE_URL=sqlite:///./app.db
```

### Using the Database

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

1. Create project with Docker:
```bash
fastinit init my-api --db --docker
cd my-api
```

2. Start services:
```bash
docker-compose up
```

3. Access application:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Using Docker Only

1. Build image:
```bash
docker build -t my-api .
```

2. Run container:
```bash
docker run -p 8000:8000 my-api
```

### Production Deployment

Update `Dockerfile` for production:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## Best Practices

### 1. Project Structure

Keep your code organized:
- **Models** (`app/models/`) - Database models
- **Schemas** (`app/schemas/`) - Pydantic validation models
- **Services** (`app/services/`) - Business logic
- **Routes** (`app/api/routes/`) - API endpoints
- **Core** (`app/core/`) - Configuration and utilities

### 2. Environment Variables

- **Never commit `.env`** to version control
- Always use `.env.example` as a template
- Use different `.env` files for dev/staging/production

### 3. Security

- Change `SECRET_KEY` in production
- Use strong passwords for database
- Enable HTTPS in production
- Implement rate limiting
- Validate all input data

### 4. Database Migrations

Use Alembic for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head
```

### 5. Testing

Write tests for your endpoints:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### 6. API Documentation

Your FastAPI app automatically generates documentation:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

## Troubleshooting

### Issue: Module Import Errors

**Solution:**
```bash
# Ensure you're in the project directory
cd my-api

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Database Connection Failed

**Solution:**
1. Verify database is running
2. Check `DATABASE_URL` in `.env`
3. Test connection manually
4. Check firewall settings

### Issue: Port Already in Use

**Solution:**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Issue: JWT Token Verification Failed

**Solution:**
1. Check `SECRET_KEY` is set correctly
2. Verify token hasn't expired
3. For JWKS, check `JWKS_URL` is accessible
4. Verify `ISSUER` and `AUDIENCE` match

### Issue: Docker Build Fails

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Getting Help

1. Check the generated `README.md` in your project
2. Review API documentation at `/docs`
3. Check logs: `docker-compose logs` (for Docker)
4. Run tests: `pytest`

---

## Advanced Usage

### Custom Templates

You can modify templates in `fastinit/templates/` to customize generated code.

### Multiple Environments

Create different env files:
- `.env.development`
- `.env.staging`
- `.env.production`

Load with:
```python
from dotenv import load_dotenv
import os

env = os.getenv("ENVIRONMENT", "development")
load_dotenv(f".env.{env}")
```

### API Versioning

Add version prefix in routes:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")
```

---

## Summary

fastinit provides a complete solution for bootstrapping FastAPI applications with:
- ✅ Quick project initialization
- ✅ Database integration
- ✅ JWT authentication
- ✅ Code generation
- ✅ Docker support
- ✅ Best practices built-in

Start building amazing APIs today! 🚀
