import pytest
from infrastructure.repositories.finance.in_memory_finance_repository import (
    InMemoryFinanceRepository,
)


@pytest.fixture
def repo():
    return InMemoryFinanceRepository()
