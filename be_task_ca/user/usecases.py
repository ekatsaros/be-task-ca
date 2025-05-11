import datetime
from uuid import UUID
from fastapi import HTTPException
from .domain.models import User, CartItem
from .domain.exceptions import UserNotFoundError, UserAlreadyExistsError
from .interfaces.repositories import UserRepository
from .schemas import (
    CreateUserRequest,
    CreateUserResponse,
    AddToCartRequest,
    AddToCartResponse,
)


class UserUseCases:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """Create a new user"""
        try:
            # Check if user exists
            if await self._repository.find_user_by_email(request.email):
                raise UserAlreadyExistsError(f"Email '{request.email}' already registered")

            # Create user
            user = User(
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
                hashed_password=request.password,  # In a real app, hash the password
                shipping_address=request.shipping_address
            )

            created_user = await self._repository.save_user(user)

            return CreateUserResponse(
                id=created_user.id,
                email=created_user.email,
                first_name=created_user.first_name,
                last_name=created_user.last_name,
                shipping_address=created_user.shipping_address,
                created_at=datetime.datetime.now()  # Assuming created_at is the current date
            )

        except UserAlreadyExistsError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def add_to_cart(self, user_id: UUID, request: AddToCartRequest) -> AddToCartResponse:
        """Add item to user's cart"""
        try:
            user = await self._repository.find_user_by_id(user_id)
            if not user:
                raise UserNotFoundError(f"User with id {user_id} not found")

            cart_item = user.add_to_cart(
                item_id=request.item_id,
                quantity=request.quantity
            )
            user.cart_items.append(cart_item)

            return AddToCartResponse(
                user_id=user_id,
                items=[
                    AddToCartRequest(
                        item_id=item.item_id,
                        quantity=item.quantity
                    ) for item in user.cart_items
                ]
            )
        except UserNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_cart(self, user_id: UUID) -> AddToCartResponse:
        """Get user's cart"""
        try:
            user = await self._repository.find_user_by_id(user_id)
            if not user:
                raise UserNotFoundError(f"User with id {user_id} not found")

            return AddToCartResponse(
                user_id=user_id,
                items=[
                    AddToCartRequest(
                        item_id=item.item_id,
                        quantity=item.quantity
                    ) for item in user.cart_items
                ]
            )

        except UserNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))