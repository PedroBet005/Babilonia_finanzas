import pytest
from tests.fakes.in_memory_finance_repository import (
    InMemoryFinanceRepository,
)


@pytest.fixture
def repo():
    return InMemoryFinanceRepository()
