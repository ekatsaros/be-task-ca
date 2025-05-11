import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from ... import app
from ..domain.models import Item
from ..schemas import CreateItemRequest, CreateItemResponse
from fastapi import FastAPI
from ..api import item_router

def get_application() -> FastAPI:
    """Create FastAPI application with all configurations"""
    app = FastAPI(title="Item API")
    app.include_router(item_router)
    return app

app = get_application()

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def valid_item_payload() -> dict:
    return {
        "name": "Test Item",
        "description": "Test Description",
        "price": "10.99",
        "quantity": 5
    }


class TestItemAPI:
    def test_create_item_success(self, client: TestClient, valid_item_payload: dict):
        # Act
        response = client.post("/items/", json=valid_item_payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == valid_item_payload["name"]
        assert data["description"] == valid_item_payload["description"]
        # assert Decimal(data["price"]) == Decimal(valid_item_payload["price"])
        assert data["quantity"] == valid_item_payload["quantity"]
        assert "id" in data
        # assert "created_at" in data

    def test_create_duplicate_item_returns_409(self, client: TestClient, valid_item_payload: dict):
        # Arrange
        client.post("/items/", json=valid_item_payload)

        # Act
        response = client.post("/items/", json=valid_item_payload)

        # Assert
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    @pytest.fixture(autouse=False)
    def test_get_all_items_returns_empty_list(self, client: TestClient):
        # Act
        response = client.get("/items/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 0

    def test_get_all_items_returns_items(self, client: TestClient, valid_item_payload: dict):
        # Arrange
        client.post("/items/", json=valid_item_payload)

        # Act
        response = client.get("/items/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        item = data["items"][0]
        assert item["name"] == valid_item_payload["name"]

    def test_create_item_invalid_data(self, client: TestClient):
        # Arrange
        invalid_payload = {
            "name": "",  # Empty name should fail validation
            "description": "Test Description",
            "price": "tsirco",  # Negative price should fail validation
            "quantity": -1  # Negative quantity should fail validation
        }

        # Act
        response = client.post("/items/", json=invalid_payload)

        # Assert
        assert response.status_code == 422