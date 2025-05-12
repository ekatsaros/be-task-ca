from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

@dataclass
class CartItem:
    item_id: UUID
    quantity: int


@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str] = None
    cart_items: List[CartItem] = field(default_factory=list)
    id: UUID = None
    created_at: datetime = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_to_cart(self, item_id: UUID, quantity: int) -> CartItem:
        """Add item to cart"""
        cart_item = CartItem(
            item_id=item_id,
            quantity=quantity
        )
        self.cart_items.append(cart_item)
        return cart_item

    def get_cart_items(self) -> List[CartItem]:
        """Get all cart items"""
        return self.cart_items
