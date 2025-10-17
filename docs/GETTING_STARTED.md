# 🚀 fastinit - Getting Started

## Welcome to fastinit!

fastinit is a powerful CLI tool that bootstraps FastAPI applications with best practices. This guide will help you get started in minutes.

## ⚡ Quick Start (30 seconds)

```bash
# 1. Install fastinit
pip install -e .

# 2. Create your first project
fastinit init my-api

# 3. Run it
cd my-api
python -m venv venv
venv\Scripts\activate  # Windows (or source venv/bin/activate on Unix)
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Visit http://localhost:8000/docs
```

Done! You have a working FastAPI application! 🎉

## 🎯 Common Use Cases

### 1. Simple REST API

```bash
fastinit init simple-api
cd simple-api
# ... setup and run
```

### 2. API with Database

```bash
fastinit init api-with-db --db --db-type postgresql
cd api-with-db
# Configure .env with database credentials
# ... setup and run
```

### 3. Authenticated API

```bash
fastinit init secure-api --jwt --logging
cd secure-api
# ... setup and run
```

### 4. Complete Production-Ready API

```bash
fastinit init production-api --db --jwt --logging --docker
cd production-api
docker-compose up
```

## 🎨 Generate Components

Once you have a project, generate code:

```bash
# Generate a complete CRUD setup
fastinit new crud User --fields "name:str,email:str,age:int"

# This creates:
# ✅ app/models/user.py - SQLAlchemy model
# ✅ app/services/user_service.py - Business logic
# ✅ app/api/routes/users.py - REST endpoints
```

Your API now has:
- `GET /users` - List users
- `GET /users/{id}` - Get user
- `POST /users` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

## 📚 What You Get

Every generated project includes:

### ✅ Project Structure
```
my-api/
├── app/
│   ├── main.py           # FastAPI application
│   ├── api/              # API routes
│   ├── core/             # Configuration
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── schemas/          # Pydantic models
├── tests/                # Tests
├── .env.example          # Environment template
└── requirements.txt      # Dependencies
```

### ✅ Features
- FastAPI application with auto-generated docs
- Health check endpoints
- Environment-based configuration
- CORS support
- Clean architecture

### ✅ Optional Features
- **Database**: PostgreSQL, MySQL, or SQLite with SQLAlchemy
- **JWT Auth**: PyJWT + PyJWKClient for secure authentication
- **Logging**: Structured logging configuration
- **Docker**: Ready-to-deploy containers

## 🔐 JWT Authentication Example

When you use `--jwt`:

```python
# In your routes
from fastapi import Depends
from app.api.deps import get_current_user

@router.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"message": f"Hello {user['sub']}!"}
```

## 🗄️ Database Example

When you use `--db`:

```python
# In your routes
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## 📖 Documentation

Generated projects include:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🐳 Docker Deployment

With `--docker` flag:

```bash
# Start everything
docker-compose up

# Your API is now running at http://localhost:8000
# Database is automatically set up
```

## 🎓 Learn By Example

Run the demo to see all features:

```bash
# Windows
.\demo.ps1

# Unix/Mac
chmod +x demo.sh
./demo.sh
```

This creates example projects with different configurations.

## 📚 Further Reading

- **QUICKSTART.md** - Detailed quick start guide
- **USAGE_GUIDE.md** - Complete usage documentation
- **README.md** - Full feature list
- **examples/** - Code examples

## 🆘 Need Help?

### Common Issues

**Q: Import errors when running the app?**
```bash
# Make sure you installed requirements
pip install -r requirements.txt
```

**Q: Database connection fails?**
```bash
# Check your .env file
# Ensure database is running
# Verify credentials
```

**Q: Port 8000 already in use?**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Check Generated README

Every project includes a README.md with specific instructions.

## 🚀 You're Ready!

You now know how to:
- ✅ Create FastAPI projects
- ✅ Add database support
- ✅ Add JWT authentication
- ✅ Generate code (models, services, routes)
- ✅ Deploy with Docker

**Start building!** 🎉

```bash
fastinit init my-awesome-api --db --jwt --logging --docker
cd my-awesome-api
docker-compose up
# Visit http://localhost:8000/docs
```

Happy coding! 💻
