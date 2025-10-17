# Examples

This directory contains example usage of fastinit CLI.

## Example Files

### Programmatic Usage (`programmatic_usage.py`)

See `programmatic_usage.py` for an example of using fastinit programmatically in Python.

```bash
python examples/programmatic_usage.py
```

### CLI Examples (`cli_examples.py`)

See `cli_examples.py` for examples of using the fastinit CLI.

```bash
python examples/cli_examples.py
```

### Pagination Examples (`pagination_examples.py`)

Examples of different pagination strategies and implementations for FastAPI endpoints.

### Alembic Integration (`alembic_example.py`)

Demonstrates how to use Alembic migrations with automatic database settings import from pydantic_settings.

```bash
python examples/alembic_example.py
```

## Quick Examples

### Basic Project

```bash
fastinit init my-api
cd my-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Project with Database

```bash
fastinit init my-api --db --db-type postgresql
cd my-api
# Configure .env file with database credentials
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Project with JWT Auth

```bash
fastinit init my-api --jwt
cd my-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Full-Featured Project

```bash
fastinit init my-api --db --jwt --logging --docker
cd my-api
docker-compose up
```

### Generate CRUD Components

```bash
cd my-api
fastinit new crud User --fields "name:str,email:str,age:int,is_active:bool"
# This creates:
# - app/models/user.py
# - app/services/user_service.py
# - app/api/routes/users.py
```

### Interactive Mode

```bash
fastinit init my-api --interactive
# Answer the prompts to configure your project
```
