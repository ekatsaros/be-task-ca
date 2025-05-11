import pytest
from uuid import UUID
from ..domain.models import User, CartItem
from ..domain.exceptions import UserNotFoundError, UserAlreadyExistsError
from ..interfaces.repositories import UserRepository


@pytest.mark.asyncio
class TestInMemoryUserRepository:
    async def test_save_user_generates_id(self, repository: UserRepository) -> None:
        # Arrange
        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password123"
        )

        # Act
        saved_user = await repository.save_user(user)

        # Assert
        assert isinstance(saved_user.id, UUID)
        assert saved_user.email == "test@example.com"

    async def test_save_duplicate_email_raises_error(self, repository: UserRepository) -> None:
        # Arrange
        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password123"
        )
        await repository.save_user(user)

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError) as exc:
            duplicate_user = User(
                email="test@example.com",
                first_name="Another",
                last_name="User",
                hashed_password="different_password"
            )
            await repository.save_user(duplicate_user)

    async def test_find_by_email_returns_user(self, repository: UserRepository) -> None:
        # Arrange
        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            hashed_password="hashed_password123"
        )
        await repository.save_user(user)

        # Act
        found_user = await repository.find_user_by_email("test@example.com")

        # Assert
        assert found_user is not None
        assert found_user.email == user.email