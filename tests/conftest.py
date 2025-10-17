"""Test configuration for pytest."""

import pytest
from pathlib import Path


@pytest.fixture
def temp_project_dir(tmp_path):
    """Provide a temporary directory for test projects."""
    return tmp_path / "test_projects"


@pytest.fixture(autouse=True)
def cleanup_temp_projects(temp_project_dir):
    """Clean up temporary test projects after each test."""
    yield
    # Cleanup happens automatically with tmp_path
