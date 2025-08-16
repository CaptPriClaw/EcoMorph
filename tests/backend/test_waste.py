# tests/backend/test_waste.py

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.main import app
from backend.app.models.user import UserRole

client = TestClient(app)

@pytest.fixture(scope="module")
def uploader_auth_token():
    """A pytest fixture to create an uploader user and get an auth token."""
    email = "test.uploader@example.com"
    password = "uploaderpassword"
    client.post("/users/", json={"email": email, "full_name": "Test Uploader", "password": password, "role": UserRole.UPLOADER})
    login_response = client.post("/token", data={"username": email, "password": password})
    token = login_response.json()["access_token"]
    return token

def test_create_waste_submission(uploader_auth_token):
    """Tests that an authenticated uploader can submit a waste item."""
    headers = {"Authorization": f"Bearer {uploader_auth_token}"}
    response = client.post(
        "/waste/",
        headers=headers,
        json={"material_type": "plastic", "description": "A plastic bottle.", "image_url": "http://example.com/bottle.jpg"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["material_type"] == "plastic"
    assert data["status"] == "pending_verification"

def test_read_my_submissions(uploader_auth_token):
    """Tests that a user can retrieve their own submissions."""
    headers = {"Authorization": f"Bearer {uploader_auth_token}"}
    response = client.get("/waste/my-submissions", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)