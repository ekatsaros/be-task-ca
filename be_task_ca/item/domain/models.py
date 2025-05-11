from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

@dataclass
class Item:
    name: str
    description: str
    price: Decimal
    quantity: int
    id: UUID | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.now()
