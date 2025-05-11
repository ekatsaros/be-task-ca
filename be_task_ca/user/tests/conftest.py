import pytest
from ..interfaces.repositories import UserRepository
from ..infrastructure.repositories import InMemoryUserRepository
from ..usecases import UserUseCases

@pytest.fixture
def repository() -> UserRepository:
    return InMemoryUserRepository()

@pytest.fixture
def use_cases(repository: UserRepository) -> UserUseCases:
    return UserUseCases(repository)