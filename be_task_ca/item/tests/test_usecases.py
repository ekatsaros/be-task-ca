import pytest
from fastapi import HTTPException
from ..usecases import ItemUseCases
from ..schemas import CreateItemRequest

@pytest.mark.asyncio
class TestItemUseCases:
    async def test_create_item_should_succeed(
        self,
        item_usecases: ItemUseCases,
        sample_item_request: CreateItemRequest
    ):
        # Act
        result = await item_usecases.create_item(sample_item_request)

        # Assert
        assert result.name == sample_item_request.name
        assert result.price == sample_item_request.price
        assert result.id is not None

    async def test_create_duplicate_item_should_raise_409(
        self,
        item_usecases: ItemUseCases,
        sample_item_request: CreateItemRequest
    ):
        # Arrange
        await item_usecases.create_item(sample_item_request)

        # Act/Assert
        with pytest.raises(HTTPException) as exc:
            await item_usecases.create_item(sample_item_request)
        assert exc.value.status_code == 409

    async def test_get_all_items_should_return_all_items(
        self,
        item_usecases: ItemUseCases,
        sample_item_request: CreateItemRequest
    ):
        # Arrange
        await item_usecases.create_item(sample_item_request)

        # Act
        result = await item_usecases.get_all_items()

        # Assert
        assert len(result.items) == 1
        assert result.items[0].name == sample_item_request.name