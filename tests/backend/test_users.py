# tests/backend/test_users.py

import sys
import os
from fastapi.testclient import TestClient

# This block adds the project's root directory to Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.main import app

client = TestClient(app)

def test_create_user_successfully():
    """Tests that a new user can be created with a valid payload."""
    response = client.post(
        "/users/",
        json={"email": "test.user@example.com", "full_name": "Test User", "password": "a-strong-password"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test.user@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_with_existing_email():
    """Tests that the API prevents creating a user with an email that already exists."""
    response = client.post(
        "/users/",
        json={"email": "test.user@example.com", "full_name": "Another User", "password": "another-password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}