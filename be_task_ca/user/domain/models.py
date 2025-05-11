from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

@dataclass
class CartItem:
    user_id: UUID
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
        """Add item to user's cart"""
        cart_item = CartItem(
            user_id=self.id,
            item_id=item_id,
            quantity=quantity
        )
        self.cart_items.append(cart_item)
        return cart_item

    def update_cart_item(self, item_id: UUID, quantity: int) -> Optional[CartItem]:
        """Update quantity of item in cart"""
        for item in self.cart_items:
            if item.item_id == item_id:
                item.quantity = quantity
                return item
        return None

    def remove_from_cart(self, item_id: UUID) -> bool:
        """Remove item from cart"""
        initial_length = len(self.cart_items)
        self.cart_items = [item for item in self.cart_items if item.item_id != item_id]
        return len(self.cart_items) < initial_length