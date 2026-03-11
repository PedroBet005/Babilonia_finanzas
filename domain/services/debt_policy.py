CONSUMPTION_DEBTS = {
    "consumption",
    "luxury",
    "appearance",
    "leisure",
    "card",
}


class DebtPolicy:
    MIN_SAVINGS_PCT = 0.10

    @classmethod
    def can_acquire_new_debt(
        cls,
        has_active_debts: bool,
        savings_pct: float,
        debt_type: str,
    ) -> tuple[bool, str | None]:

        if has_active_debts:
            return False, "alert_existing_debts"

        if savings_pct < cls.MIN_SAVINGS_PCT:
            return False, "alert_low_savings"

        if debt_type.lower() in CONSUMPTION_DEBTS:
            return False, "alert_consumption_debt"

        return True, None
