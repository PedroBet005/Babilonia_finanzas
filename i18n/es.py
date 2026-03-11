MESSAGES = {

    # ===============================
    # 🌍 Idioma / General
    # ===============================
    "welcome": "¡Bienvenido a Finanzas de Babilonia!",
    "select_language": "Seleccione idioma",
    "spanish": "Español",
    "english": "Inglés",

    # ===============================
    # 📜 Menús
    # ===============================
    "main_menu": "MENÚ PRINCIPAL",
    "menu_income": "Registrar ingreso",
    "menu_expense": "Registrar gasto",
    "menu_balance": "Ver balance",
    "menu_change_language": "Cambiar idioma",
    "financial_tools": "Herramientas financieras",
    "exit": "Salir",
    "back": "Volver",
    "select_option": "Selecciona una opción",

    # ===============================
    # 💰 Ingresos / Gastos
    # ===============================
    "enter_amount": "Ingresa el monto",
    "enter_source": "Concepto del ingreso",
    "income": "Ingresos",
    "expense": "Gastos",
    "income_saved": "✅ Ingreso registrado con éxito",
    "expense_saved": "Gasto registrado correctamente",
    "amount_must_be_positive": "El monto debe ser mayor que cero",
    "invalid_amount": "Monto inválido",

    # ===============================
    # 📊 Balance
    # ===============================
    "balance_title": "📊 RESUMEN FINANCIERO BABILÓNICO",
    "tithe": "Diezmo",
    "debts": "Deudas",
    "savings": "Ahorro (regla de Babilonia – 10%)",
    "available": "Gasto disponible",
    "amount": "Monto",
    "total": "Total",
    "grand_total": "Total general",

    # ===============================
    # 🧾 Herramientas financieras
    # ===============================
    "monthly_report": "Reporte mensual del oro",
    "period_summary": "Resumen por períodos",
    "cash_flow": "Flujo del tesoro",
    "babylon_savings": "Ahorro babilónico (10%)",
    "financial_evolution": "Evolución financiera",

    # ===============================
    # 📤 Exportaciones
    # ===============================
    "export_reports": "Exportar / Imprimir reportes",
    "export_txt": "Exportar a TXT",
    "export_csv": "Exportar a CSV",
    "export_monthly_txt": "Exportar reporte mensual (TXT)",
    "export_monthly_csv": "Exportar reporte mensual (CSV)",
    "export_financial_evolution": "Exportar evolución financiera",
    "export_financial_chart": "Exportar gráfica de evolución financiera",
    "export_expenses_by_category": "Exportar gastos por categoría",
    "menu_export_babylon_savings": "Exportar ahorro babilónico",
    "file_generated": "Archivo generado correctamente",
    "expenses_by_category": "Gastos por categoría",
    "no_data_for_period": "No hay movimientos registrados para el período seleccionado.",
    "no_expenses_for_period": "No hay gastos registrados para el período seleccionado.",
    "no_income_for_period": "No hay ingresos registrados para el período seleccionado.",


    


    # ===============================
    # 📅 Fechas / Períodos
    # ===============================
    "enter_month": "📅 Mes (1-12): ",
    "enter_year": "📆 Año (YYYY): ",
    "period": "Período",

    # ===============================
    # 📂 Categorías de gastos
    # ===============================
    "expense_category": "Categoría del gasto",
    "select_category_option": "👉 Selecciona una opción: ",
    "enter_expense_name": "✏️ Nombre del gasto: ",
    "enter_expense_amount": "💸 Monto del gasto: ",
    "enter_description": "📝 Descripción: ",
    "category": "Categoría",
    "others": "Otros",

    "cat_food": "Alimentación",
    "cat_children": "Hijos(as)",
    "cat_social": "Aportes sociales",
    "cat_fuel": "Combustible",
    "cat_vehicle": "Vehículo",
    "cat_utilities": "Servicios públicos",
    "cat_operational": "Operativos",
    "cat_project": "Proyecto productivo",
    "cat_leisure": "Ocio",
    "cat_other": "Otros",

    # ===============================
    # 🏺 Ahorro babilónico
    # ===============================
    "total_savings": "Ahorro acumulado",
    "monthly_savings": "Ahorro del período",
    "average_savings": "Promedio mensual de ahorro",
    "savings_success": "Una parte de todo lo que ganas es tuya. Vas por buen camino.",
    "savings_warning": "Recuerda: una parte de todo lo que ganas debe ser tuya.",

    # ===============================
    # ℹ️ Estados / Errores
    # ===============================
    "no_data": "ℹ️ Aún no hay movimientos registrados para este período",
    "invalid_option": "Opción no válida. Intenta nuevamente",
    "feature_coming_soon": "🚧 Función en desarrollo. Muy pronto estará disponible",

    # ===============================
    # 📆 Meses
    # ===============================
    "month_names": {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    },

    "apply_tithes": "¿Aplicar al diezmo? (s/n): ",
    "apply_debts": "¿Aplicar a deudas? (s/n): ",
    "yes_key": "s",
    "invalid_year": "Año inválido. Usa formato YYYY (ej: 2024)",
    "invalid_month": "Mes inválido. Ingresa un valor entre 1 y 12",
    "no_data_for_period": "No hay movimientos registrados para el período seleccionado",
    "no_income_for_period": "No hay ingresos registrados en este período. El resultado puede ser negativo",



}


def t(key):
    return MESSAGES.get(key, key)
