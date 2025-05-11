import pytest
from typing import Coroutine, Any
from uuid import UUID
from ..domain.models import Item
from ..interfaces.repositories import ItemRepository
from ..domain.exceptions import ItemAlreadyExistsError

@pytest.mark.asyncio
class TestInMemoryItemRepository:
    async def test_save_item_should_generate_id(self, repository: ItemRepository) -> None:
        # Arrange
        item = Item(
            name="Test Item",
            description="Test Description",
            price=10.99,
            quantity=5
        )

        # Act
        saved_item = await repository.save_item(item)

        # Assert
        assert isinstance(saved_item.id, UUID)
        assert saved_item.name == "Test Item"

    async def test_find_item_by_name_should_return_item(self, repository: ItemRepository) -> None:
        # Arrange
        item = Item(
            name="Test Item",
            description="Test Description",
            price=10.99,
            quantity=5
        )
        await repository.save_item(item)

        # Act
        found_item = await repository.find_item_by_name("Test Item")

        # Assert
        assert found_item is not None
        assert found_item.name == "Test Item"

    async def test_get_all_items_should_return_all_items(self, repository: ItemRepository) -> None:
        # Arrange
        items = [
            Item(name="Item 1", description="Desc 1", price=10.99, quantity=5),
            Item(name="Item 2", description="Desc 2", price=20.99, quantity=3)
        ]
        for item in items:
            await repository.save_item(item)

        # Act
        result = await repository.get_all_items()

        # Assert
        assert len(result) == 2


    async def test_find_item_by_id_should_return_item(self, repository: ItemRepository) -> None:
        # Arrange
        item = Item(
            name="Test Item",
            description="Test Description",
            price=10.99,
            quantity=5
        )
        saved_item = await repository.save_item(item)

        # Act
        found_item = await repository.find_item_by_id(saved_item.id)

        # Assert
        assert found_item is not None
        assert found_item.id == saved_item.id