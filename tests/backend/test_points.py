# tests/backend/test_points.py

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def new_user_auth_token():
    """A pytest fixture to create a brand new user for point testing."""
    email = "test.points.user@example.com"
    password = "pointspassword"
    client.post("/users/", json={"email": email, "full_name": "Points User", "password": password})
    login_response = client.post("/token", data={"username": email, "password": password})
    token = login_response.json()["access_token"]
    return token

def test_get_my_balance_initially(new_user_auth_token):
    """Tests that a new user's balance is initially zero."""
    headers = {"Authorization": f"Bearer {new_user_auth_token}"}
    response = client.get("/points/my-balance", headers=headers)
    assert response.status_code == 200
    # Assuming no signup bonus, the initial balance should be 0.
    assert response.json()["current_balance"] == 0

def test_get_my_history_initially(new_user_auth_token):
    """Tests that a new user's point history is initially empty."""
    headers = {"Authorization": f"Bearer {new_user_auth_token}"}
    response = client.get("/points/my-history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []