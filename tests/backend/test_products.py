# tests/backend/test_products.py

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.main import app
from backend.app.models.user import UserRole

client = TestClient(app)


@pytest.fixture(scope="module")
def upcycler_auth_token():
    """A pytest fixture to create an upcycler user and get an auth token."""
    # Create a unique email for the test user
    email = "test.upcycler@example.com"
    password = "upcyclerpassword"

    # Register the user
    client.post("/users/",
                json={"email": email, "full_name": "Test Upcycler", "password": password, "role": UserRole.UPCYCLER})

    # Log in to get the token
    login_response = client.post("/token", data={"username": email, "password": password})
    token = login_response.json()["access_token"]
    return token


def test_create_product_authenticated(upcycler_auth_token):
    """Tests that an authenticated upcycler can create a product."""
    headers = {"Authorization": f"Bearer {upcycler_auth_token}"}
    response = client.post(
        "/products/",
        headers=headers,
        json={"name": "Test Bottle Lamp", "description": "A lamp from a bottle.",
              "image_url": "http://example.com/lamp.jpg", "price_points": 100}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Bottle Lamp"


def test_create_product_unauthenticated():
    """Tests that an unauthenticated user cannot create a product."""
    response = client.post(
        "/products/",
        json={"name": "Unauthorized Lamp", "description": "This should fail.",
              "image_url": "http://example.com/fail.jpg", "price_points": 50}
    )
    assert response.status_code == 401


def test_browse_marketplace():
    """Tests that anyone can browse the marketplace."""
    response = client.get("/marketplace/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # The response should be a list of products