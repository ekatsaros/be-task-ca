import pytest
from uuid import UUID
from fastapi import HTTPException
from ..usecases import UserUseCases
from ..schemas import CreateUserRequest, AddToCartRequest


@pytest.mark.asyncio
class TestUserUseCases:
    async def test_create_user_success(self, use_cases: UserUseCases) -> None:
        # Arrange
        request = CreateUserRequest(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
            shipping_address="123 Test St"
        )

        # Act
        result = await use_cases.create_user(request)

        # Assert
        assert isinstance(result.id, UUID)
        assert result.email == request.email
        assert result.first_name == request.first_name

    async def test_create_duplicate_user_raises_409(self, use_cases: UserUseCases) -> None:
        # Arrange
        request = CreateUserRequest(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        await use_cases.create_user(request)

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await use_cases.create_user(request)
        assert exc.value.status_code == 409

    async def test_add_to_cart_success(self, use_cases: UserUseCases) -> None:
        # Arrange
        user = await use_cases.create_user(CreateUserRequest(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        ))

        cart_request = AddToCartRequest(
            item_id=UUID('a7e75788-a2e6-4f7f-b54d-b9f3214a4e89'),
            quantity=2
        )

        # Act
        result = await use_cases.add_to_cart(user.id, cart_request)

        # Assert
        assert result.user_id == user.id
        assert len(result.items) == 1
        assert result.items[0].quantity == cart_request.quantity
