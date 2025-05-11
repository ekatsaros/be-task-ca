import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from uuid import uuid4
from ..api import user_router


def get_application() -> FastAPI:
    """Create FastAPI application with all configurations"""
    app = FastAPI(title="Item API")
    app.include_router(user_router)
    return app


test_app = get_application()


@pytest.fixture
def client() -> TestClient:
    return TestClient(test_app)



@pytest.fixture
def valid_user_data():
    return {
        "email": f"test_{uuid4()}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123",
        "shipping_address": "123 Test St"
    }


class TestUserAPI:
    def test_create_user_success(self, client: TestClient, valid_user_data: dict):
        # Act
        response = client.post("/users/", json=valid_user_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == valid_user_data["email"]
        assert "id" in data

    def test_create_duplicate_user_returns_409(self, client: TestClient, valid_user_data: dict):
        # Arrange
        client.post("/users/", json=valid_user_data)

        # Act
        response = client.post("/users/", json=valid_user_data)

        # Assert
        assert response.status_code == 409

    def test_add_to_cart_success(self, client: TestClient, valid_user_data: dict):
        # Arrange

        user_response = client.post("/users/", json=valid_user_data)
        user_id = user_response.json()["id"]

        cart_data = {
            "item_id": str(uuid4()),
            "quantity": 2
        }

        # Act
        response = client.post(f"/users/{user_id}/cart", json=cart_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert len(data["items"]) == 1
        # assert data["items"][0]["quantity"] == cart_data["quantity"]