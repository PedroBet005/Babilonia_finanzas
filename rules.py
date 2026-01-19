RULES = {
    "max_gastos_pct": 0.6,     # 60% del ingreso
    "min_ahorro_pct": 0.1,     # 10% mínimo
    "alerta_ocio_pct": 0.2     # +20% vs mes anterior
}


RULES_NO_DEBT = {
    "diezmo": 0.10,
    "mi_pago": 0.10,
    "gastos": 0.80
}

RULES_WITH_DEBT = {
    "diezmo": 0.10,
    "mi_pago": 0.10,
    "deudas": 0.10,
    "gastos": 0.70
}

EXPENSE_CATEGORIES = [
    "Alimentación",
    "Hijas",
    "Combustible",
    "Vehiculo",
    "Servicios Publicos",
    "Educación",
    "Aportes sociales",
    "Proyecto productivo",
    "Gastos operativos",
    "Ocio",
    "Otros"
]


