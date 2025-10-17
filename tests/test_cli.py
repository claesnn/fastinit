"""Tests for the fastinit CLI."""

from typer.testing import CliRunner

from fastinit.cli import app

runner = CliRunner()


def test_version():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "FastInit" in result.stdout


def test_init_basic(tmp_path):
    """Test basic project initialization."""
    project_name = "test-project"
    result = runner.invoke(app, ["init", project_name, "--output", str(tmp_path)])

    # Check if command succeeded
    assert result.exit_code == 0

    # Check if project directory was created
    project_dir = tmp_path / project_name
    assert project_dir.exists()

    # Check if essential files were created
    assert (project_dir / "app" / "main.py").exists()
    assert (project_dir / "app" / "core" / "config.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".env.example").exists()
    assert (project_dir / "README.md").exists()


def test_init_with_db(tmp_path):
    """Test project initialization with database."""
    project_name = "test-db-project"
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

    project_dir = tmp_path / project_name
    assert (project_dir / "app" / "db" / "session.py").exists()
    assert (project_dir / "app" / "db" / "base.py").exists()


def test_init_with_jwt(tmp_path):
    """Test project initialization with JWT."""
    project_name = "test-jwt-project"
    result = runner.invoke(app, ["init", project_name, "--output", str(tmp_path), "--jwt"])

    assert result.exit_code == 0

    project_dir = tmp_path / project_name
    assert (project_dir / "app" / "core" / "security.py").exists()


def test_init_with_docker(tmp_path):
    """Test project initialization with Docker."""
    project_name = "test-docker-project"
    result = runner.invoke(app, ["init", project_name, "--output", str(tmp_path), "--docker"])

    assert result.exit_code == 0

    project_dir = tmp_path / project_name
    assert (project_dir / "Dockerfile").exists()
    assert (project_dir / "docker-compose.yml").exists()


def test_init_all_features(tmp_path):
    """Test project initialization with all features."""
    project_name = "test-full-project"
    result = runner.invoke(
        app,
        [
            "init",
            project_name,
            "--output",
            str(tmp_path),
            "--db",
            "--jwt",
            "--logging",
            "--docker",
        ],
    )

    assert result.exit_code == 0

    project_dir = tmp_path / project_name
    assert (project_dir / "app" / "db" / "session.py").exists()
    assert (project_dir / "app" / "core" / "security.py").exists()
    assert (project_dir / "Dockerfile").exists()
