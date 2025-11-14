"""Pytest configuration and shared fixtures."""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_user_dir(tmp_path):
    """Create temporary directory for test user files."""
    users_dir = tmp_path / "users"
    users_dir.mkdir()
    return users_dir


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "alice": {
            "nom": "Alice Dupont",
            "grade": "CM2",
            "score": 850
        },
        "bob": {
            "nom": "Bob Martin",
            "grade": "CM1",
            "score": 720
        }
    }


@pytest.fixture
def cleanup_json_files(tmp_path):
    """Cleanup JSON files after test."""
    yield tmp_path
    # Cleanup code here if needed
