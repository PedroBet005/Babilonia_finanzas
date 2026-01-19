
def distribute_income(amount, has_debt, pays_tithe):

    tithe  = amount * 0.10 if pays_tithe else 0

    if has_debt:
        return {
            "Diezmo": tithe,
            "Mi pago": amount * 0.10,
            "Deudas": amount * 0.10,
            "Gastos": amount * 0.70
        }
    else:
        return {
            "Diezmo": tithe,
            "Mi pago": amount * 0.10,
            "Gastos": amount * 0.80
        }



