from typing import Dict, List, Optional
from uuid import UUID
from ..domain.models import User, CartItem
from ..domain.exceptions import UserAlreadyExistsError
from ..interfaces.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: Dict[UUID, User] = {}

    async def save_user(self, user: User) -> User:
        # Check for existing users
        if await self.find_user_by_id(user.id):
            raise UserAlreadyExistsError(f"User with id '{user.id}' already exists")
        if await self.find_user_by_email(user.email):
            raise UserAlreadyExistsError(f"User with email '{user.email}' already exists")

        self._users[user.id] = user
        return user

    async def find_user_by_email(self, email: str) -> Optional[User]:
        return next(
            (user for user in self._users.values() if user.email == email),
            None
        )

    async def find_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self._users.get(user_id)

    async def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        user = await self.find_user_by_id(user_id)
        if user:
            return user.cart_items
        return []

