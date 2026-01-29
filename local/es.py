MESSAGES = {
    "welcome": "¡Bienvenido a Finanzas de Babilonia!",

    "main_menu": "MENÚ PRINCIPAL",
    "menu_income": "Registrar ingreso",
    "menu_expense": "Registrar gasto",
    "menu_balance": "Ver balance",
    "menu_change_language": "Cambiar idioma",
    "exit": "Salir",

    "select_option": "Selecciona una opción",
    "invalid_option": "Opción inválida, intenta nuevamente",

    "income_saved": "Ingreso guardado correctamente",
    "expense_saved": "Gasto registrado correctamente",

    "amount_must_be_positive": "El monto debe ser mayor que cero",
    "period_closed": "El período está cerrado",

    "enter_amount": "Ingresa el monto",
    "enter_source": "Concepto del ingreso",

    "balance_title": "📊 RESUMEN FINANCIERO BABILÓNICO",

    "savings": "Ahorro (regla de Babilonia – 10%)",
    "tithe": "Diezmo",
    "debts": "Deudas",
    "available": "Gasto disponible",

    "financial_tools": "Herramientas financieras",
    "financial_tools_title": "HERRAMIENTAS FINANCIERAS",
    "monthly_report": "Reporte mensual del oro",
    "period_summary": "Resumen por períodos",
    "expenses_by_category": "Gastos por categoría",
    "cash_flow": "Flujo del tesoro",
    "babylon_savings": "Ahorro babilónico (10%)",
    "financial_evolution": "Evolución financiera",
    "export_reports": "Exportar / Imprimir reportes",
    "back": "Volver",
    "feature_coming_soon": "Funcionalidad en desarrollo",

    "monthly_report": "Reporte mensual del oro",
    "income": "Ingresos",
    "expense": "Gastos",

    "export_monthly_txt": "Exportar reporte mensual (TXT)",
    "export_monthly_csv": "Exportar reporte mensual (CSV)",
    "file_generated": "Archivo generado correctamente",

    "expenses_by_category": "Gastos por categoría",
    "total": "Total",
    "no_data": "No hay datos para este período",
    "others": "Otros",

    "export_txt": "Exportar a TXT",
    "export_csv": "Exportar a CSV",
    "cash_flow": "Flujo del tesoro",


    "babylon_savings": "Ahorro babilónico (10%)",
    "total_savings": "Ahorro acumulado",
    "monthly_savings": "Ahorro del período",
    "average_savings": "Promedio mensual de ahorro",
    "savings_success": "Una parte de todo lo que ganas es tuya. Vas por buen camino.",
    "savings_warning": "Recuerda: una parte de todo lo que ganas debe ser tuya.",
    "menu_financial_evolution": "Evolución financiera",
    "financial_evolution_title": "📈 Evolución financiera del oro",

    "export_success": "Reporte exportado correctamente",
    "export_error": "Error al exportar el reporte",

    "financial_tools": "Herramientas financieras",
    "menu_export_evolution": "Exportar evolución financiera",
    "back": "Volver",

    "expenses_by_category": "Gastos por categoría",
    "period": "Período",
    "percentage": "Porcentaje",
    "amount": "Monto",
    "others": "Otros",


}


def t(key):
    return MESSAGES.get(key, key)
