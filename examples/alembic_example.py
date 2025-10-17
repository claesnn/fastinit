"""
Example: Using Alembic with Automatic Settings Import

This example demonstrates how to use Alembic migrations in a FastInit project
with automatic database URL import from pydantic_settings.
"""

# Step 1: Initialize a new project with database support
# Run in terminal:
# $ fastinit init my-api --db --db-type postgresql

# Step 2: Configure your database URL in .env
# Edit .env file:
# DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Step 3: Create a model (example: User model)
# File: app/models/user.py
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
"""

# Step 4: Import model in app/models/__init__.py
"""
from app.models.user import User

__all__ = ["User"]
"""

# Step 5: Generate migration
# Alembic automatically reads DATABASE_URL from settings!
# Run in terminal:
# $ alembic revision --autogenerate -m "Add users table"

# Output will show:
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.autogenerate.compare] Detected added table 'users'
# Generating /path/to/alembic/versions/xxx_add_users_table.py ... done

# Step 6: Apply migration
# Run in terminal:
# $ alembic upgrade head

# Output:
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL.
# INFO  [alembic.runtime.migration] Running upgrade  -> xxx, Add users table

# Step 7: Verify in your application
# File: app/main.py (example)
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

app = FastAPI(title=settings.PROJECT_NAME)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post("/users")
def create_user(email: str, full_name: str, db: Session = Depends(get_db)):
    user = User(email=email, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
"""

# Key Benefits:
# ✅ No manual configuration of database URL in alembic.ini
# ✅ Single source of truth: DATABASE_URL in .env
# ✅ Same settings used by app and migrations
# ✅ Easy to switch between environments (dev, staging, prod)

# Advanced: Multiple Environments
# Create different .env files:
# .env.development:
"""
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/dev_db
"""

# .env.production:
"""
DATABASE_URL=postgresql://prod_user:prod_pass@prod-host:5432/prod_db
"""

# Load appropriate environment in app/core/config.py:
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    
    class Config:
        env_file = os.getenv("ENV_FILE", ".env.development")
        case_sensitive = True

settings = Settings()
"""

# Then run migrations for different environments:
# $ ENV_FILE=.env.development alembic upgrade head  # Dev
# $ ENV_FILE=.env.production alembic upgrade head   # Production

print("✨ Alembic with automatic settings import is ready to use!")
print("📖 See docs/ALEMBIC_INTEGRATION.md for more details")
