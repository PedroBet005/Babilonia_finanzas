REGLAS = {
    "max_gastos_pct": 0.6,     # 60% del ingreso
    "min_ahorro_pct": 0.1,     # 10% mínimo
    "alerta_ocio_pct": 0.2     # +20% vs mes anterior
}


REGLAS_SIN_DEUDAS = {
    "diezmo": 0.10,
    "mi_pago": 0.10,
    "gastos": 0.80
}

REGLAS_CON_DEUDAS = {
    "diezmo": 0.10,
    "mi_pago": 0.10,
    "deudas": 0.10,
    "gastos": 0.70
}

CATEGORIAS_GASTOS = [
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

