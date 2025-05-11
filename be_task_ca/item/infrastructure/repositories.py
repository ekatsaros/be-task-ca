from typing import List, Optional, Dict
from uuid import UUID
from ..domain.models import Item
from ..interfaces.repositories import ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self._items: Dict[UUID, Item] = {}

    async def save_item(self, item: Item) -> Item:
        self._items[item.id] = item
        return item

    async def get_all_items(self) -> List[Item]:
        return list(self._items.values())

    async def find_item_by_name(self, name: str) -> Optional[Item]:
        return next(
            (item for item in self._items.values() if item.name == name),
            None
        )

    async def find_item_by_id(self, id: UUID) -> Optional[Item]:
        return self._items.get(id)