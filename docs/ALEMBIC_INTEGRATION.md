# Alembic Integration with Pydantic Settings

## Overview

FastInit now automatically configures Alembic to import database settings from your application's `pydantic_settings` Settings class. This eliminates the need to manually configure database URLs in multiple places and ensures consistency between your application and migration configurations.

## Key Features

- **Automatic Settings Import**: Alembic reads `DATABASE_URL` directly from `app.core.config.settings`
- **DRY Principle**: Single source of truth for database configuration
- **Environment-Based**: Works seamlessly with `.env` files
- **Zero Manual Configuration**: No need to edit `alembic.ini` with database credentials

## How It Works

### Settings Class (app/core/config.py)

Your pydantic_settings configuration:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Alembic Environment (alembic/env.py)

The Alembic environment is automatically configured to import and use these settings:

```python
from app.core.config import settings
from app.db.base import Base

def get_url():
    """Get database URL from settings."""
    return settings.DATABASE_URL

def run_migrations_online():
    """Run migrations with settings from pydantic_settings."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()  # Override with settings
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # ... rest of migration logic
```

## Usage

### 1. Initialize Project with Database Support

```bash
fastinit init myproject --db --db-type postgresql
cd myproject
```

### 2. Configure Environment

Copy and edit your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` to set your database URL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

### 3. Create Models

Create SQLAlchemy models in `app/models/`:

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
```

Make sure to import in `app/models/__init__.py`:

```python
from app.models.user import User
```

### 4. Generate Migration

```bash
alembic revision --autogenerate -m "Add users table"
```

Alembic will automatically:
- Read `DATABASE_URL` from your `.env` file via `settings`
- Detect your models
- Generate the migration script

### 5. Apply Migration

```bash
alembic upgrade head
```

## Benefits

### Before (Manual Configuration)

You had to:
1. Set `DATABASE_URL` in `.env`
2. Edit `alembic.ini` to set `sqlalchemy.url`
3. Keep both in sync manually
4. Risk configuration drift

### After (Automatic Import)

You only need to:
1. Set `DATABASE_URL` in `.env`
2. Run migrations

The database URL is automatically imported from your application settings!

## Different Database Types

The configuration works with any database supported by SQLAlchemy:

### SQLite
```env
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### MySQL
```env
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

## Advanced Configuration

### Multiple Environments

Use different `.env` files for different environments:

```bash
# Development
.env.development
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/dev_db

# Production
.env.production
DATABASE_URL=postgresql://prod_user:prod_pass@prod-host:5432/prod_db
```

Load the appropriate one:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    
    class Config:
        env_file = ".env.production"  # or .env.development
        case_sensitive = True
```

### Custom Settings Path

If you use a custom settings location, update `alembic/env.py`:

```python
# Instead of:
from app.core.config import settings

# Use your custom import:
from custom.path.config import settings
```

## Troubleshooting

### ImportError: No module named 'app'

Make sure you're running Alembic from the project root directory where the `app` folder is located.

### Can't locate revision identified by

This usually means you haven't run any migrations yet:

```bash
alembic upgrade head
```

### Settings not loading from .env

Ensure:
1. `.env` file exists in the project root
2. `python-dotenv` is installed
3. Your `Settings` class has `env_file = ".env"` in the Config

## File Structure

When database support is enabled, FastInit generates:

```
myproject/
├── alembic/                 # Alembic migration directory
│   ├── versions/            # Migration scripts go here
│   ├── env.py               # Auto-imports settings ✨
│   ├── script.py.mako       # Migration template
│   └── README.md            # Migration documentation
├── alembic.ini              # Alembic configuration
├── app/
│   ├── core/
│   │   └── config.py        # Settings class with DATABASE_URL
│   ├── db/
│   │   ├── base.py          # SQLAlchemy Base
│   │   └── session.py       # Database session
│   └── models/              # SQLAlchemy models
│       └── __init__.py
└── .env                     # Environment variables (DATABASE_URL)
```

## Examples

See the `alembic/README.md` file in your generated project for additional usage examples and migration commands.

## Testing

Run the test suite to verify Alembic configuration:

```bash
pytest tests/test_generated_projects.py::test_alembic_configuration_generated
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
