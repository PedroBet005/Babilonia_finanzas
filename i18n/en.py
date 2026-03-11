MESSAGES = {

    # ===============================
    # 🌍 Language / General
    # ===============================
    "welcome": "Welcome to Babylon Finance!",
    "select_language": "Select language",
    "spanish": "Spanish",
    "english": "English",

    # ===============================
    # 📜 Menus
    # ===============================
    "main_menu": "MAIN MENU",
    "menu_income": "Register income",
    "menu_expense": "Register expense",
    "menu_balance": "View balance",
    "menu_change_language": "Change language",
    "financial_tools": "Financial tools",
    "exit": "Exit",
    "back": "Back",
    "select_option": "Select an option",

    # ===============================
    # 💰 Income / Expenses
    # ===============================
    "enter_amount": "Enter amount",
    "enter_source": "Income concept",
    "income": "Income",
    "expense": "Expenses",
    "income_saved": "✅ Income successfully registered",
    "expense_saved": "Expense successfully registered",
    "amount_must_be_positive": "Amount must be greater than zero",
    "invalid_amount": "Invalid amount",

    # ===============================
    # 📊 Balance
    # ===============================
    "balance_title": "📊 BABYLONIAN FINANCIAL SUMMARY",
    "tithe": "Tithe",
    "debts": "Debts",
    "savings": "Savings (Babylon rule – 10%)",
    "available": "Available spending",
    "amount": "Amount",
    "total": "Total",
    "grand_total": "Grand total",

    # ===============================
    # 🧾 Financial tools
    # ===============================
    "monthly_report": "Monthly gold report",
    "period_summary": "Period summary",
    "cash_flow": "Cash flow",
    "babylon_savings": "Babylonian savings (10%)",
    "financial_evolution": "Financial evolution",

    # ===============================
    # 📤 Exports
    # ===============================
    "export_reports": "Export / Print reports",
    "export_txt": "Export to TXT",
    "export_csv": "Export to CSV",
    "export_monthly_txt": "Export monthly report (TXT)",
    "export_monthly_csv": "Export monthly report (CSV)",
    "export_financial_evolution": "Export financial evolution",
    "export_financial_chart": "Export financial evolution chart",
    "export_expenses_by_category": "Export expenses by category",
    "menu_export_babylon_savings": "Export Babylonian savings",
    "file_generated": "File successfully generated",
    "expenses_by_category": "Expenses by category",
    "no_data_for_period": "No transactions found for the selected period.",
    "no_expenses_for_period": "No expenses recorded for the selected period.",
    "no_income_for_period": "No income recorded for the selected period.",
    




    # ===============================
    # 📅 Dates / Periods
    # ===============================
    "enter_month": "📅 Month (1-12): ",
    "enter_year": "📆 Year (YYYY): ",
    "period": "Period",

    # ===============================
    # 📂 Expense categories
    # ===============================
    "expense_category": "Expense category",
    "select_category_option": "👉 Select an option: ",
    "enter_expense_name": "✏️ Expense name: ",
    "enter_expense_amount": "💸 Expense amount: ",
    "enter_description": "📝 Description: ",
    "category": "Category",
    "others": "Others",

    "cat_food": "Food",
    "cat_children": "Children",
    "cat_social": "Social contributions",
    "cat_fuel": "Fuel",
    "cat_vehicle": "Vehicle",
    "cat_utilities": "Utilities",
    "cat_operational": "Operational",
    "cat_project": "Productive project",
    "cat_leisure": "Leisure",
    "cat_other": "Others",

    # ===============================
    # 🏺 Babylonian savings
    # ===============================
    "total_savings": "Total savings",
    "monthly_savings": "Period savings",
    "average_savings": "Average monthly savings",
    "savings_success": "A part of everything you earn is yours. You're on the right path.",
    "savings_warning": "Remember: a part of everything you earn must be yours.",

    # ===============================
    # ℹ️ Status / Errors
    # ===============================
    "no_data": "ℹ️ No data available for this period",
    "invalid_option": "Invalid option. Please try again",
    "feature_coming_soon": "🚧 Feature under development. Coming soon",

    # ===============================
    # 📆 Months
    # ===============================
    "month_names": {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    },


    "apply_tithes": "Apply tithe? (y/n): ",
    "apply_debts": "Apply to debts? (y/n): ",
    "yes_key": "y",
    "invalid_year": "Invalid year. Use YYYY format (e.g. 2024)",
    "invalid_month": "Invalid month. Enter a value between 1 and 12",
    "no_data_for_period": "No transactions found for the selected period",
    "no_income_for_period": "No income registered for this period. The result may be negative",




}


def t(key):
    return MESSAGES.get(key, key)



 