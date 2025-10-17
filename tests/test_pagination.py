"""Tests for pagination feature in code generation."""

import pytest
from typer.testing import CliRunner

from fastinit.cli import app

runner = CliRunner()


@pytest.fixture
def test_project(tmp_path):
    """Create a test FastAPI project."""
    project_name = "test-pagination-project"
    result = runner.invoke(
        app,
        [
            "init",
            project_name,
            "--output",
            str(tmp_path),
            "--db",
            "--db-type",
            "postgresql",
        ],
    )
    assert result.exit_code == 0
    return tmp_path / project_name


def test_route_with_limit_offset_pagination(test_project):
    """Test route generation with default limit-offset pagination."""
    result = runner.invoke(
        app,
        ["new", "route", "users", "--project-dir", str(test_project)],
    )
    assert result.exit_code == 0

    route_file = test_project / "app" / "api" / "routes" / "users.py"
    assert route_file.exists()

    content = route_file.read_text()
    assert "skip: int = 0" in content
    assert "limit: int = 100" in content
    assert "skip=skip, limit=limit" in content


def test_route_with_explicit_limit_offset_pagination(test_project):
    """Test route generation with explicit limit-offset pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "route",
            "products",
            "--project-dir",
            str(test_project),
            "--pagination",
            "limit-offset",
        ],
    )
    assert result.exit_code == 0

    route_file = test_project / "app" / "api" / "routes" / "products.py"
    assert route_file.exists()

    content = route_file.read_text()
    assert "skip: int = 0" in content
    assert "limit: int = 100" in content


def test_route_with_cursor_pagination(test_project):
    """Test route generation with cursor pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "route",
            "orders",
            "--project-dir",
            str(test_project),
            "--pagination",
            "cursor",
        ],
    )
    assert result.exit_code == 0

    route_file = test_project / "app" / "api" / "routes" / "orders.py"
    assert route_file.exists()

    content = route_file.read_text()
    assert "cursor: Optional[int] = None" in content
    assert "limit: int = 100" in content
    assert "cursor=cursor, limit=limit" in content
    assert "from typing import List, Optional" in content


def test_route_with_no_pagination(test_project):
    """Test route generation with no pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "route",
            "categories",
            "--project-dir",
            str(test_project),
            "--pagination",
            "none",
        ],
    )
    assert result.exit_code == 0

    route_file = test_project / "app" / "api" / "routes" / "categories.py"
    assert route_file.exists()

    content = route_file.read_text()
    assert "skip:" not in content
    assert "limit:" not in content
    assert "cursor:" not in content
    # Should only have db dependency
    assert "db: Session = Depends(get_db)" in content


def test_service_with_limit_offset_pagination(test_project):
    """Test service generation with limit-offset pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "service",
            "UserService",
            "--project-dir",
            str(test_project),
            "--model",
            "User",
        ],
    )
    assert result.exit_code == 0

    service_file = test_project / "app" / "services" / "user_service.py"
    assert service_file.exists()

    content = service_file.read_text()
    assert "skip: int = 0, limit: int = 100" in content
    assert "offset(skip).limit(limit)" in content


def test_service_with_cursor_pagination(test_project):
    """Test service generation with cursor pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "service",
            "ProductService",
            "--project-dir",
            str(test_project),
            "--model",
            "Product",
            "--pagination",
            "cursor",
        ],
    )
    assert result.exit_code == 0

    service_file = test_project / "app" / "services" / "product_service.py"
    assert service_file.exists()

    content = service_file.read_text()
    assert "cursor: Optional[int] = None, limit: int = 100" in content
    assert "if cursor:" in content
    assert "filter(Product.id > cursor)" in content
    assert "order_by(Product.id)" in content


def test_service_with_no_pagination(test_project):
    """Test service generation with no pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "service",
            "CategoryService",
            "--project-dir",
            str(test_project),
            "--model",
            "Category",
            "--pagination",
            "none",
        ],
    )
    assert result.exit_code == 0

    service_file = test_project / "app" / "services" / "category_service.py"
    assert service_file.exists()

    content = service_file.read_text()
    assert "def get_all(db: Session) -> List[Category]:" in content
    assert "skip" not in content
    assert "limit" not in content
    assert "cursor" not in content


def test_crud_with_cursor_pagination(test_project):
    """Test CRUD generation with cursor pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "crud",
            "Post",
            "--project-dir",
            str(test_project),
            "--fields",
            "title:str,content:text",
            "--pagination",
            "cursor",
        ],
    )
    assert result.exit_code == 0

    # Check service file
    service_file = test_project / "app" / "services" / "post_service.py"
    assert service_file.exists()
    service_content = service_file.read_text()
    assert "cursor: Optional[int] = None" in service_content
    assert "filter(Post.id > cursor)" in service_content

    # Check route file
    route_file = test_project / "app" / "api" / "routes" / "posts.py"
    assert route_file.exists()
    route_content = route_file.read_text()
    assert "cursor: Optional[int] = None" in route_content
    assert "cursor=cursor, limit=limit" in route_content


def test_crud_with_no_pagination(test_project):
    """Test CRUD generation with no pagination."""
    result = runner.invoke(
        app,
        [
            "new",
            "crud",
            "Tag",
            "--project-dir",
            str(test_project),
            "--fields",
            "name:str",
            "--pagination",
            "none",
        ],
    )
    assert result.exit_code == 0

    # Check service file
    service_file = test_project / "app" / "services" / "tag_service.py"
    assert service_file.exists()
    service_content = service_file.read_text()
    assert "def get_all(db: Session) -> List[Tag]:" in service_content

    # Check route file
    route_file = test_project / "app" / "api" / "routes" / "tags.py"
    assert route_file.exists()
    route_content = route_file.read_text()
    assert "skip:" not in route_content
    assert "cursor:" not in route_content


def test_invalid_pagination_type(test_project):
    """Test that invalid pagination type is rejected."""
    result = runner.invoke(
        app,
        [
            "new",
            "route",
            "invalid",
            "--project-dir",
            str(test_project),
            "--pagination",
            "invalid-type",
        ],
    )
    assert result.exit_code == 1
    assert "Invalid pagination type" in result.stdout


def test_component_generator_pagination_api():
    """Test ComponentGenerator pagination_type parameter API."""
    # This test verifies the API interface
    from fastinit.generators.component import ComponentGenerator

    # Verify the methods have the pagination_type parameter
    import inspect

    sig = inspect.signature(ComponentGenerator.generate_route)
    assert "pagination_type" in sig.parameters
    assert sig.parameters["pagination_type"].default == "limit-offset"

    sig = inspect.signature(ComponentGenerator.generate_service)
    assert "pagination_type" in sig.parameters
    assert sig.parameters["pagination_type"].default == "limit-offset"
