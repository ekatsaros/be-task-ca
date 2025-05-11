import pytest
from decimal import Decimal
from ..interfaces.repositories import ItemRepository
from ..infrastructure.repositories import InMemoryItemRepository
from ..usecases import ItemUseCases
from ..schemas import CreateItemRequest

@pytest.fixture
def repository() -> ItemRepository:
    """Provides a clean repository for each test"""
    return InMemoryItemRepository()

@pytest.fixture
def item_usecases(repository: ItemRepository) -> ItemUseCases:
    """Provides use cases with a clean repository"""
    return ItemUseCases(repository)

@pytest.fixture
def sample_item_request() -> CreateItemRequest:
    """Provides a sample item request"""
    return CreateItemRequest(
        name="Test Item",
        description="Test Description",
        price=Decimal("10.99"),
        quantity=5
    )
