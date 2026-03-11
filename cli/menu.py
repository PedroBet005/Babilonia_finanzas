from datetime import datetime

from app.local.lang import t, set_language
from app.services.financie.logic import (
    register_income,
    load_data,
    save_data,
)

from app.services.reports.reports_service import (
    export_financial_evolution_txt,
    export_financial_evolution_chart,
    export_expenses_by_category_txt,
    export_babylon_savings_txt,
)


# ==========================================================
# Helpers
# ==========================================================

def _handle_service_result(result):
    if result["status"] == "ok":
        print(f"✅ {t('export_success')}: {result['file']}")
    elif result["status"] == "no_data":
        print("ℹ️", t(result["message_key"]))
    else:
        print("❌", t("export_error"))
        if "error" in result:
            print(result["error"])


# ==========================================================
# Init & Language
# ==========================================================

def init_app():
    print("\n🌍 " + t("select_language"))
    print("1️⃣ " + t("spanish"))
    print("2️⃣ " + t("english"))

    choice = input("👉 ").strip()
    set_language("en" if choice == "2" else "es")

    print(t("welcome"))


def handle_change_language():
    init_app()


# ==========================================================
# Main Menu
# ==========================================================

def show_menu():
    while True:
        print("\n📜", t("main_menu"))
        print("1️⃣ ", t("menu_income"))
        print("2️⃣ ", t("menu_expense"))
        print("3️⃣ ", t("menu_balance"))
        print("4️⃣ ", t("menu_change_language"))
        print("5️⃣ ", t("financial_tools"))
        print("6️⃣ ", t("exit"))

        option = input("👉 " + t("select_option") + ": ").strip()

        if option == "1":
            handle_register_income()
        elif option == "2":
            handle_register_expense()
        elif option == "3":
            show_balance()
        elif option == "4":
            handle_change_language()
        elif option == "5":
            show_financial_tools_menu()
        elif option == "6":
            break
        else:
            print("❌", t("invalid_option"))


# ==========================================================
# Income / Expense
# ==========================================================

def handle_register_income():
    try:
        amount = float(input(t("enter_amount")))
    except ValueError:
        print("❌", t("invalid_amount"))
        return

    source = input(t("enter_source"))
    apply_tithe = input(t("apply_tithes")).strip().lower() == t("yes_key")
    apply_debt = input(t("apply_debts")).strip().lower() == t("yes_key")

    result = register_income(
        amount,
        source,
        apply_tithe=apply_tithe,
        apply_debt=apply_debt,
    )

    if result.get("status") == "ok":
        print("\n✅", t("income_registered_successfully"))
        print("─" * 40)
        print(f"💰 {t('income')}: {result['income']:,.2f}")
        print(f"🏺 {t('savings')}: {result['savings']:,.2f}")
        print(f"🙏 {t('tithe')}: {result['tithe']:,.2f}")
        print(f"🧾 {t('debts')}: {result['debts']:,.2f}")
        print(f"🟢 {t('available')}: {result['available']:,.2f}")
        print("─" * 40)
    else:
        print("❌", t("error"))
        if "error" in result:
            print(t(result["error"]))



def handle_register_expense():
    data = load_data()

    print("\n➖ " + t("register_expense_title"))

    categories = [
        t("cat_food"),
        t("cat_children"),
        t("cat_social"),
        t("cat_fuel"),
        t("cat_vehicle"),
        t("cat_utilities"),
        t("cat_operational"),
        t("cat_project"),
        t("cat_leisure"),
        t("cat_other"),
    ]

    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    try:
        choice = int(input(t("select_category_option")))
        category = categories[choice - 1]
    except (ValueError, IndexError):
        print("❌", t("invalid_option"))
        return

    if category == t("cat_other"):
        category = input(t("enter_expense_name"))

    try:
        amount = float(input(t("enter_expense_amount")))
    except ValueError:
        print("❌", t("invalid_amount"))
        return

    description = input(t("enter_description"))

    data.setdefault("expenses", []).append({
        "category": category,
        "amount": amount,
        "description": description,
        "date": datetime.now().isoformat(),
    })

    save_data(data)
    print("✅", t("expense_saved"))


# ==========================================================
# Balance
# ==========================================================

def show_balance():
    data = load_data()
    summary = data.get("summary", {})

    print("\n" + t("balance_title"))
    print("─" * 40)

    print(f"🙏 {t('tithe')}: {summary.get('tithe', 0):.2f}")
    print(f"🧾 {t('debts')}: {summary.get('debts', 0):.2f}")
    print(f"🏦 {t('savings')}: {summary.get('savings', 0):.2f}")

    available = (
        summary.get("income", 0)
        - summary.get("tithe", 0)
        - summary.get("debts", 0)
        - summary.get("savings", 0)
    )

    print("─" * 40)
    print(f"💰 {t('available')}: {available:.2f}")


# ==========================================================
# Financial Tools
# ==========================================================

def show_financial_tools_menu():
    while True:
        print("\n🧾 " + t("financial_tools"))

        print("1️⃣ ", t("export_financial_evolution"))
        print("2️⃣ ", t("export_financial_chart"))
        print("3️⃣ ", t("export_expenses_by_category"))
        print("4️⃣ ", t("menu_export_babylon_savings"))
        print("0️⃣ ", t("back"))

        option = input("👉 " + t("select_option") + ": ").strip()

        if option == "1":
            _handle_service_result(export_financial_evolution_txt())
        elif option == "2":
            _handle_service_result(export_financial_evolution_chart())
        elif option == "3":
            _handle_service_result(export_expenses_by_category_txt())
        elif option == "4":
            _handle_service_result(export_babylon_savings_txt())
        elif option == "0":
            break
        else:
            print("❌", t("invalid_option"))


# ==========================================================
# Entry point
# ==========================================================

def main():
    init_app()
    show_menu()


if __name__ == "__main__":
    main()
