def distribute_income(amount, has_debt, pays_tithe):

    tithe = amount * 0.10 if pays_tithe else 0

    if has_debt:
        return {
            "tithe": tithe,
            "my_payment": amount * 0.10,
            "debts": amount * 0.10,
            "expenses": amount * 0.70
        }
    else:
        return {
            "tithe": tithe,
            "my_payment": amount * 0.10,
            "expenses": amount * 0.80
        }

