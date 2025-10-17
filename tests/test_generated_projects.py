"""Tests for generated project functionality."""

from typer.testing import CliRunner

from fastinit.cli import app

runner = CliRunner()


def test_generated_project_structure(tmp_path):
    """Test that generated project has correct structure."""
    project_name = "test-structure"
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db", "--jwt"]
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Check main directories
    assert (project_dir / "app").is_dir()
    assert (project_dir / "app" / "api").is_dir()
    assert (project_dir / "app" / "core").is_dir()
    assert (project_dir / "app" / "db").is_dir()
    assert (project_dir / "app" / "models").is_dir()
    assert (project_dir / "app" / "schemas").is_dir()
    assert (project_dir / "app" / "services").is_dir()
    assert (project_dir / "tests").is_dir()

    # Check key files
    assert (project_dir / "app" / "main.py").is_file()
    assert (project_dir / "app" / "core" / "config.py").is_file()
    assert (project_dir / "app" / "core" / "security.py").is_file()
    assert (project_dir / "app" / "db" / "session.py").is_file()
    assert (project_dir / "app" / "api" / "routes" / "health.py").is_file()
    assert (project_dir / "requirements.txt").is_file()
    assert (project_dir / ".env.example").is_file()


def test_generated_project_imports(tmp_path):
    """Test that generated project has valid Python imports."""
    project_name = "test-imports"
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Test if main.py is valid Python
    main_file = project_dir / "app" / "main.py"
    content = main_file.read_text()

    # Check for key imports (without app. prefix since we run from app directory)
    assert "from fastapi import FastAPI" in content
    assert "from core.config import settings" in content


def test_component_generation(tmp_path):
    """Test component generation in a project."""
    project_name = "test-components"

    # Create project
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )
    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Generate model
    result = runner.invoke(
        app,
        [
            "new",
            "model",
            "TestModel",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,age:int",
        ],
    )
    assert result.exit_code == 0
    assert (project_dir / "app" / "models" / "testmodel.py").is_file()

    # Generate schema
    result = runner.invoke(
        app,
        [
            "new",
            "schema",
            "TestModel",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,age:int",
        ],
    )
    assert result.exit_code == 0
    assert (project_dir / "app" / "schemas" / "testmodel.py").is_file()

    # Generate service
    result = runner.invoke(
        app,
        [
            "new",
            "service",
            "TestService",
            "--project-dir",
            str(project_dir),
            "--model",
            "TestModel",
        ],
    )
    assert result.exit_code == 0
    assert (project_dir / "app" / "services" / "test_service.py").is_file()

    # Generate route
    result = runner.invoke(
        app,
        [
            "new",
            "route",
            "tests",
            "--project-dir",
            str(project_dir),
            "--service",
            "TestService",
        ],
    )
    assert result.exit_code == 0
    assert (project_dir / "app" / "api" / "routes" / "tests.py").is_file()


def test_crud_generation(tmp_path):
    """Test CRUD generation."""
    project_name = "test-crud"

    # Create project
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )
    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Generate CRUD
    result = runner.invoke(
        app,
        [
            "new",
            "crud",
            "Product",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,price:float",
        ],
    )
    assert result.exit_code == 0

    # Check all generated files
    assert (project_dir / "app" / "models" / "product.py").is_file()
    assert (project_dir / "app" / "schemas" / "product.py").is_file()
    assert (project_dir / "app" / "services" / "product_service.py").is_file()
    assert (project_dir / "app" / "api" / "routes" / "products.py").is_file()

    # Verify schema content includes Pydantic models
    schema_file = project_dir / "app" / "schemas" / "product.py"
    schema_content = schema_file.read_text()
    assert "ProductCreate" in schema_content
    assert "ProductUpdate" in schema_content
    assert "ProductResponse" in schema_content
    assert "from pydantic import BaseModel" in schema_content
    assert "model_config = ConfigDict(from_attributes=True)" in schema_content

    # Verify route imports schemas instead of just dicts
    route_file = project_dir / "app" / "api" / "routes" / "products.py"
    route_content = route_file.read_text()
    assert "from schemas.product import" in route_content
    assert "ProductCreate" in route_content
    assert "ProductUpdate" in route_content
    assert "ProductResponse" in route_content
    assert "response_model=List[ProductResponse]" in route_content
    assert "response_model=ProductResponse" in route_content


def test_database_types(tmp_path):
    """Test different database type configurations."""
    for db_type in ["postgresql", "mysql", "sqlite"]:
        project_name = f"test-db-{db_type}"
        result = runner.invoke(
            app,
            [
                "init",
                project_name,
                "--output",
                str(tmp_path),
                "--db",
                "--db-type",
                db_type,
            ],
        )
        assert result.exit_code == 0

        project_dir = tmp_path / project_name
        env_file = project_dir / ".env.example"
        content = env_file.read_text()

        if db_type == "sqlite":
            assert "sqlite" in content.lower()
        elif db_type == "postgresql":
            assert "postgresql" in content.lower()
        elif db_type == "mysql":
            assert "mysql" in content.lower()


def test_alembic_configuration_generated(tmp_path):
    """Test that Alembic configuration files are generated correctly."""
    project_name = "test-alembic"
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Check Alembic files exist
    assert (project_dir / "alembic.ini").is_file()
    assert (project_dir / "alembic").is_dir()
    assert (project_dir / "alembic" / "env.py").is_file()
    assert (project_dir / "alembic" / "script.py.mako").is_file()
    assert (project_dir / "alembic" / "README.md").is_file()
    assert (project_dir / "alembic" / "versions").is_dir()

    # Check that env.py imports settings correctly
    env_file = project_dir / "alembic" / "env.py"
    env_content = env_file.read_text()

    assert "from app.core.config import settings" in env_content
    assert "settings.DATABASE_URL" in env_content
    assert "from app.db.base import Base" in env_content
    assert "target_metadata = Base.metadata" in env_content

    # Check alembic.ini has correct script location
    alembic_ini = project_dir / "alembic.ini"
    ini_content = alembic_ini.read_text()
    assert "script_location = alembic" in ini_content


def test_alembic_not_generated_without_db(tmp_path):
    """Test that Alembic files are not generated when database is not enabled."""
    project_name = "test-no-alembic"
    result = runner.invoke(app, ["init", project_name, "--output", str(tmp_path)])

    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Check Alembic files don't exist
    assert not (project_dir / "alembic.ini").exists()
    assert not (project_dir / "alembic").exists()


def test_docker_generation(tmp_path):
    """Test Docker file generation."""
    project_name = "test-docker"
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--docker"]
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name
    assert (project_dir / "Dockerfile").is_file()
    assert (project_dir / "docker-compose.yml").is_file()
    assert (project_dir / ".dockerignore").is_file()


def test_jwt_configuration(tmp_path):
    """Test JWT configuration in generated project."""
    project_name = "test-jwt-config"
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--jwt"]
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Check security.py exists
    security_file = project_dir / "app" / "core" / "security.py"
    assert security_file.is_file()

    content = security_file.read_text()
    assert "PyJWT" in content or "jwt" in content
    assert "create_access_token" in content
    assert "verify_token" in content

    # Check requirements include JWT libraries
    req_file = project_dir / "requirements.txt"
    req_content = req_file.read_text()
    assert "PyJWT" in req_content
    assert "PyJWKClient" in req_content


def test_duplicate_file_prevention(tmp_path):
    """Test that generating duplicate files raises an error."""
    project_name = "test-duplicates"

    # Create project
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )
    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Generate model first time - should succeed
    result = runner.invoke(
        app,
        [
            "new",
            "model",
            "Product",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,price:float",
        ],
    )
    assert result.exit_code == 0
    assert (project_dir / "app" / "models" / "product.py").is_file()

    # Try to generate the same model again - should fail
    result = runner.invoke(
        app,
        [
            "new",
            "model",
            "Product",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,price:float",
        ],
    )
    assert result.exit_code == 1
    assert "already exists" in result.stdout

    # Test CRUD duplicate prevention
    result = runner.invoke(
        app,
        [
            "new",
            "crud",
            "User",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,email:str",
        ],
    )
    assert result.exit_code == 0

    # Try to generate the same CRUD again - should fail
    result = runner.invoke(
        app,
        [
            "new",
            "crud",
            "User",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,email:str",
        ],
    )
    assert result.exit_code == 1
    assert "already exist" in result.stdout


def test_schema_generation(tmp_path):
    """Test standalone schema generation."""
    project_name = "test-schema"

    # Create project
    result = runner.invoke(
        app, ["init", project_name, "--output", str(tmp_path), "--db"]
    )
    assert result.exit_code == 0

    project_dir = tmp_path / project_name

    # Generate schema
    result = runner.invoke(
        app,
        [
            "new",
            "schema",
            "User",
            "--project-dir",
            str(project_dir),
            "--fields",
            "name:str,email:str,age:int,is_active:bool",
        ],
    )
    assert result.exit_code == 0

    # Check schema file was created
    schema_file = project_dir / "app" / "schemas" / "user.py"
    assert schema_file.is_file()

    # Verify content
    content = schema_file.read_text()
    assert "UserBase" in content
    assert "UserCreate" in content
    assert "UserUpdate" in content
    assert "UserResponse" in content
    assert "from pydantic import BaseModel" in content
    assert "name: str" in content
    assert "email: str" in content
    assert "age: int" in content
    assert "is_active: bool" in content
    assert "model_config = ConfigDict(from_attributes=True)" in content

    # Check schemas directory has __init__.py
    assert (project_dir / "app" / "schemas" / "__init__.py").is_file()
