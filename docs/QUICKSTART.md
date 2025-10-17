# fastinit - Quick Start Guide

## Installation

Install fastinit using pip:

```bash
pip install -e .
```

Or for development:

```bash
git clone <repository-url>
cd fastapi-starter
pip install -e .
```

## Basic Usage

### 1. Create a Simple FastAPI Project

```bash
fastinit init my-api
cd my-api
python -m venv venv
venv\Scripts\activate  # Windows (or source venv/bin/activate on Unix)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the API documentation.

### 2. Create a Project with Database

```bash
fastinit init my-api --db --db-type postgresql
cd my-api
cp .env.example .env
# Edit .env and configure your database URL
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Create a Project with JWT Authentication

```bash
fastinit init my-api --jwt
cd my-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The JWT authentication includes:
- PyJWT for token creation and verification
- PyJWKClient for remote JWK verification (optional)
- Security utilities in `app/core/security.py`
- Protected endpoint example using dependencies

### 4. Create a Full-Featured Project

```bash
fastinit init my-api --db --jwt --logging --docker
cd my-api
docker-compose up
```

### 5. Interactive Mode

Let the CLI guide you through configuration:

```bash
fastinit init my-api --interactive
```

## Generating Components

Once you have a project, you can generate components:

### Generate a Model

```bash
cd my-api
fastinit new model User --fields "name:str,email:str,age:int,is_active:bool"
```

This creates `app/models/user.py` with a SQLAlchemy model.

### Generate a Service

```bash
fastinit new service UserService --model User
```

This creates `app/services/user_service.py` with CRUD operations.

### Generate a Route

```bash
fastinit new route users --service UserService
```

This creates `app/api/routes/users.py` with REST endpoints.

### Generate Everything at Once (CRUD)

```bash
fastinit new crud Product --fields "name:str,price:float,description:text,in_stock:bool"
```

This generates:
- `app/models/product.py` - SQLAlchemy model
- `app/services/product_service.py` - Service layer
- `app/api/routes/products.py` - API endpoints

## Project Structure

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── api/
│   │   ├── deps.py                # Dependencies (DB session, auth)
│   │   └── routes/
│   │       └── health.py          # Health check endpoints
│   ├── core/
│   │   ├── config.py              # Settings with .env support
│   │   └── security.py            # JWT utilities (if --jwt)
│   ├── db/                        # (if --db)
│   │   ├── base.py                # SQLAlchemy base
│   │   └── session.py             # DB session
│   ├── models/                    # SQLAlchemy models
│   ├── schemas/                   # Pydantic schemas
│   └── services/                  # Business logic
├── tests/
├── .env.example                   # Environment template
├── .gitignore
├── requirements.txt
├── Dockerfile                     # (if --docker)
├── docker-compose.yml            # (if --docker)
└── README.md
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
PROJECT_NAME=my-api
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-change-in-production
```

## Health Endpoints

All projects include health check endpoints:

- `GET /api/health` - Basic health check
- `GET /api/health/db` - Database connectivity (if --db)
- `GET /api/health/ready` - Readiness probe (Kubernetes)
- `GET /api/health/live` - Liveness probe (Kubernetes)

## JWT Authentication

When using `--jwt`, you get:

1. **Token Creation:**
```python
from app.core.security import create_access_token

token = create_access_token({"sub": "user@example.com"})
```

2. **Protected Endpoints:**
```python
from fastapi import Depends
from app.api.deps import get_current_user

@router.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user}
```

3. **JWKS Support:**
Configure in `.env`:
```env
USE_JWKS=true
JWKS_URL=https://your-auth-provider.com/.well-known/jwks.json
ISSUER=https://your-auth-provider.com
AUDIENCE=your-api-audience
```

## Database Support

Supported databases:
- PostgreSQL (`--db-type postgresql`)
- MySQL (`--db-type mysql`)
- SQLite (`--db-type sqlite`)

## Docker Support

With `--docker` flag, you get:

- `Dockerfile` - Optimized multi-stage build
- `docker-compose.yml` - Complete stack with database
- `.dockerignore` - Optimized build context

Run with:
```bash
docker-compose up
```

## Next Steps

1. **Add more models**: `fastinit new crud ModelName`
2. **Customize settings**: Edit `app/core/config.py`
3. **Add schemas**: Create Pydantic models in `app/schemas/`
4. **Write tests**: Add tests in `tests/`
5. **Deploy**: Use the generated Dockerfile

## Common Commands

```bash
# View help
fastinit --help

# View version
fastinit version

# Init with all features
fastinit init my-api --db --jwt --logging --docker

# Generate CRUD
fastinit new crud Product --fields "name:str,price:float"

# Generate individual components
fastinit new model User
fastinit new service UserService
fastinit new route users
```

## Troubleshooting

### Database Connection Issues

Check your `DATABASE_URL` in `.env` file and ensure the database server is running.

### Import Errors

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use

Change the port in the uvicorn command:
```bash
uvicorn app.main:app --reload --port 8001
```

## Getting Help

- Check the README.md in your generated project
- Visit the API docs at `/docs` when running
- See examples in the `examples/` directory
