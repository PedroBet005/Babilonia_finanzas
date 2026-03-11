def apply_babylonian_rules(
    amount: float,
    tithe: bool = False,
    debt: bool = False,
) -> dict:
    if amount <= 0:
        raise ValueError("amount_must_be_positive")

    savings = round(amount * 0.10, 2)
    tithe_amount = round(amount * 0.10, 2) if tithe else 0.0
    debt_amount = round(amount * 0.10, 2) if debt else 0.0

    available = round(
        amount - savings - tithe_amount - debt_amount,
        2
    )

    return {
        "savings": savings,
        "tithe": tithe_amount,
        "debts": debt_amount,
        "available": available,
    }


