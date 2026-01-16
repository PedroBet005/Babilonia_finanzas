def distribuir_ingreso(monto, tiene_deudas, paga_diezmo):

    diezmo = monto * 0.10 if paga_diezmo else 0

    if tiene_deudas:
        return {
            "Diezmo": diezmo,
            "Mi pago": monto * 0.10,
            "Deudas": monto * 0.10,
            "Gastos": monto * 0.70
        }
    else:
        return {
            "Diezmo": diezmo,
            "Mi pago": monto * 0.10,
            "Gastos": monto * 0.80
        }



