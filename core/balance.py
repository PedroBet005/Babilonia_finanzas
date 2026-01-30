CONSUMPTION_DEBTS = [
    "consumo",
    "lujo",
    "apariencia",
    "ocio",
    "tarjeta",
]


def can_acquire_new_debt(
    has_active_debts,
    savings_pct,
    debt_type
):
    MIN_SAVINGS_PCT = 0.10

    # 🚫 Regla 1: ya tiene deudas
    if has_active_debts:
        return False, "alert_existing_debts"

    # 🚫 Regla 2: no ahorra mínimo
    if savings_pct < MIN_SAVINGS_PCT:
        return False, "alert_low_savings"

    # 🚫 Regla 3: deuda de consumo
    if debt_type in CONSUMPTION_DEBTS:
        return False, "alert_consumption_debt"

    return True, None



def distribute_income(amount, has_debts, pay_tithe, savings_pct=0.10):
    MIN_SAVINGS_PCT = 0.10
    DEBTS_PCT = 0.10
    TITHE_PCT = 0.10

    # 🔐 Regla de Babilonia: nunca menos del 10%
    if savings_pct < MIN_SAVINGS_PCT:
        savings_pct = MIN_SAVINGS_PCT

    distribution = {}

    distribution["tithe"] = amount * TITHE_PCT if pay_tithe else 0
    distribution["savings"] = amount * savings_pct
    distribution["debts"] = amount * DEBTS_PCT if has_debts else 0

    distribution["expenses"] = max(
        0,
        amount - (
            distribution["tithe"]
            + distribution["savings"]
            + distribution["debts"]
        )
    )

    return distribution


