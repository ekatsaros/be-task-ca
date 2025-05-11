from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..domain.models import Item


class ItemRepository(ABC):
    @abstractmethod
    async def save_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    async def get_all_items(self) -> List[Item]:
        pass

    @abstractmethod
    async def find_item_by_name(self, name: str) -> Optional[Item]:
        pass

    @abstractmethod
    async def find_item_by_id(self, id: UUID) -> Optional[Item]:
        pass