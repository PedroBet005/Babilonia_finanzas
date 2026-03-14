import pytest
from tests.fakes.in_memory_finance_repository import (
    InMemoryFinanceRepository,
)
from infrastructure.repositories.in_memory import InMemoryFinanceRepository

@pytest.fixture
def repo():
    return InMemoryFinanceRepository()
