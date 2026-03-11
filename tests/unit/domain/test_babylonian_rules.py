import pytest

from domain.services.babylonian_rules import apply_babylonian_rules


def test_amount_must_be_positive():
    with pytest.raises(ValueError, match="amount_must_be_positive"):
        apply_babylonian_rules(amount=0, tithe=False, debt=False)


def test_minimum_savings_is_10_percent():
    result = apply_babylonian_rules(amount=1000, tithe=False, debt=False)

    assert result["savings"] == 100.0
    assert result["available"] == 900.0


def test_tithe_is_applied_when_enabled():
    result = apply_babylonian_rules(amount=1000, tithe=True, debt=False)

    assert result["savings"] == 100.0
    assert result["tithe"] == 100.0
    assert result["available"] == 800.0


def test_debt_is_applied_when_enabled():
    result = apply_babylonian_rules(amount=1000, tithe=False, debt=True)

    assert result["savings"] == 100.0
    assert result["debts"] == 100.0
    assert result["available"] == 800.0


def test_full_distribution():
    result = apply_babylonian_rules(amount=1000, tithe=True, debt=True)

    assert result["savings"] == 100.0
    assert result["tithe"] == 100.0
    assert result["debts"] == 100.0
    assert result["available"] == 700.0
