from fastapi import APIRouter
from .schemas import CreateItemResponse, AllItemsResponse, CreateItemRequest
from .infrastructure.repositories import InMemoryItemRepository
from .usecases import ItemUseCases

item_router = APIRouter(prefix="/items", tags=["items"])

# Initialize repository and use cases
repository = InMemoryItemRepository()
item_usecases = ItemUseCases(repository)


@item_router.post("/", response_model=CreateItemResponse)
async def create_item(item: CreateItemRequest) -> CreateItemResponse:
    return await item_usecases.create_item(item)


@item_router.get("/", response_model=AllItemsResponse)
async def get_items() -> AllItemsResponse:
    return await item_usecases.get_all_items()