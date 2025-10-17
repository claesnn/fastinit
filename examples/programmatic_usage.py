"""Example usage of the FastInit CLI programmatically."""

from pathlib import Path
from fastinit.models.config import ProjectConfig
from fastinit.generators.project import ProjectGenerator


def create_example_project():
    """Create an example FastAPI project with all features."""

    # Configure the project
    config = ProjectConfig(
        project_name="my-awesome-api",
        output_dir=Path.cwd(),
        use_db=True,
        db_type="postgresql",
        use_jwt=True,
        use_logging=True,
        use_docker=True,
        python_version="3.11",
    )

    # Generate the project
    print(f"Generating project: {config.project_name}")
    generator = ProjectGenerator(config)
    generator.generate()

    print(f"✓ Project created at: {config.project_path}")
    print("\nNext steps:")
    print(f"  1. cd {config.project_name}")
    print("  2. python -m venv venv")
    print("  3. venv\\Scripts\\activate  # Windows")
    print("  4. pip install -r requirements.txt")
    print("  5. Copy .env.example to .env and configure")
    print("  6. uvicorn app.main:app --reload")


if __name__ == "__main__":
    create_example_project()
