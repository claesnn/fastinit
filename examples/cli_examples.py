#!/usr/bin/env python
"""Example: Create a basic FastAPI project using the CLI."""

import subprocess
import sys


def run_command(cmd):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)


def main():
    """Create example projects."""

    # Example 1: Basic project
    print("=" * 60)
    print("Example 1: Creating a basic FastAPI project")
    print("=" * 60)
    run_command(["fastinit", "init", "basic-api"])

    # Example 2: Project with database
    print("\n" + "=" * 60)
    print("Example 2: Creating a project with database support")
    print("=" * 60)
    run_command(["fastinit", "init", "db-api", "--db", "--db-type", "postgresql"])

    # Example 3: Project with JWT auth
    print("\n" + "=" * 60)
    print("Example 3: Creating a project with JWT authentication")
    print("=" * 60)
    run_command(["fastinit", "init", "auth-api", "--jwt", "--logging"])

    # Example 4: Full-featured project
    print("\n" + "=" * 60)
    print("Example 4: Creating a full-featured project")
    print("=" * 60)
    run_command(
        [
            "fastinit",
            "init",
            "full-api",
            "--db",
            "--db-type",
            "postgresql",
            "--jwt",
            "--logging",
            "--docker",
        ]
    )

    # Example 5: Generate CRUD components
    print("\n" + "=" * 60)
    print("Example 5: Generating CRUD components")
    print("=" * 60)
    run_command(
        [
            "fastinit",
            "new",
            "crud",
            "Product",
            "--project-dir",
            "full-api",
            "--fields",
            "name:str,price:float,description:text,in_stock:bool",
        ]
    )

    print("\n" + "=" * 60)
    print("All examples created successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
