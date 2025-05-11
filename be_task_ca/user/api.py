from uuid import UUID
from fastapi import APIRouter, HTTPException
from .usecases import UserUseCases
from .infrastructure.repositories import InMemoryUserRepository
from .schemas import (
    CreateUserRequest,
    CreateUserResponse,
    AddToCartRequest,
    AddToCartResponse,
)

# Initialize router
user_router = APIRouter(prefix="/users", tags=["users"])

# Initialize repository and use cases
repository = InMemoryUserRepository()
use_cases = UserUseCases(repository)


@user_router.post("/", response_model=CreateUserResponse)
async def create_user(request: CreateUserRequest) -> CreateUserResponse:
    """Create a new user"""
    try:
        return await use_cases.create_user(request)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@user_router.post("/{user_id}/cart")
async def add_to_cart(user_id: UUID, request: AddToCartRequest) -> AddToCartResponse:
    """Add item to user's cart"""
    return await use_cases.add_to_cart(user_id, request)



@user_router.get("/{user_id}/cart", response_model=AddToCartResponse)
async def get_cart(user_id: UUID) -> AddToCartResponse:
    """Get user's cart items"""
    return await use_cases.get_cart(user_id)
