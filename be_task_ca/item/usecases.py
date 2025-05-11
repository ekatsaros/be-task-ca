from fastapi import HTTPException
from .domain.models import Item
from .domain.exceptions import ItemAlreadyExistsError
from .interfaces.repositories import ItemRepository
from .schemas import CreateItemRequest, CreateItemResponse, AllItemsResponse


class ItemUseCases:
    def __init__(self, repository: ItemRepository):
        self._repository = repository

    async def create_item(self, schema: CreateItemRequest) -> CreateItemResponse:
        try:
            if await self._repository.find_item_by_name(schema.name):
                raise ItemAlreadyExistsError(f"Item with name '{schema.name}' already exists")

            item = Item(
                name=schema.name,
                description=schema.description,
                price=schema.price,
                quantity=schema.quantity
            )
            created_item = await self._repository.save_item(item)
            # Convert to dict first to handle both Pydantic v1 and v2
            return CreateItemResponse(**{
                'id': created_item.id,
                'name': created_item.name,
                'description': created_item.description,
                'price': created_item.price,
                'quantity': created_item.quantity,
            })

        except ItemAlreadyExistsError as e:
            raise HTTPException(status_code=409, detail=str(e))

    async def get_all_items(self) -> AllItemsResponse:
        items = await self._repository.get_all_items()
        return AllItemsResponse(
            items=[CreateItemResponse(**{
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'quantity': item.quantity,
            }) for item in items]
        )
