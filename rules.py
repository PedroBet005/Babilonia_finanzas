# rules.py

RULES = {
    # Gastos no deberían superar el 60% del ingreso total
    "max_expense_pct": 0.60,

    # Ahorro mínimo esperado (Regla de Babilonia – 10%)
    "min_saving_pct": 0.10,

    # Alerta si el gasto de ocio sube más del 20% vs mes anterior
    "alerta_ocio_pct": 0.20,
}


DEBT_CATEGORY_KEY = "DEUDAS"

EXPENSE_CATEGORIES = [
    "ALIMENTACION",
    "DEUDAS",
    "OCIO",
]

# Categorías de gasto (solo informativas / reportes)
EXPENSE_CATEGORIES = [
    "Alimentación",
    "Hijas",
    "Combustible",
    "Vehículo",
    "Servicios Públicos",
    "Educación",
    "Aportes sociales",
    "Proyecto productivo",
    "Gastos operativos",
    "Ocio",
    "Otros"
]



