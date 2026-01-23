
import security as security
import calculator as calculator
import matplotlib.pyplot as plt
from datetime import datetime
import copy
import csv
import shutil
import os
import json
import rules
from i18n import t




def main_menu():
    print(t("welcome"))
    # resto del menú


def run():
    main_menu()


# ⚠️ IMPORTANTE:
# Los datos reales de la aplicación se guardan en:
# C:\Users\<Usuario>\AppData\Roaming\BabiloniaFinanzas
# NO usar datos.json del proyecto ni de /dist

APP_DIR = os.path.join(os.environ["APPDATA"], "BabiloniaFinanzas")
os.makedirs(APP_DIR, exist_ok=True)

DATA_PATH = os.path.join(APP_DIR, "datos.json")
LOG_PATH = os.path.join(APP_DIR, "log.txt")


# ==============================
# CONFIGURACIÓN GENERAL 
# ==============================
TEST_MODE = False  # 🔁 Cambiar a False cuando uses datos reales


EXPENSE_CATEGORIES = [
    "category_food",
    "category_transport",
    "category_housing",
    "category_services",
    "category_education",
    "category_health",
    "category_leisure",
    "category_other"
]



def save_data(data):
    # Guardar datos en JSON y log
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"save_ok - {datetime.now()}\n")

    except Exception as e:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"save_error {e}\n")
        raise


def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # 🔒 ESTRUCTURA PRINCIPAL
    data.setdefault("income", [])
    data.setdefault("expenses", [])
    data.setdefault("goals", [])

    # 🔒 RESUMEN
    data.setdefault("summary", {})
    data["summary"].setdefault("emergency_saving", 0)
    data["summary"].setdefault("general_saving", 0)
    data["summary"].setdefault("total_saving", 0)

    # 🔒 CONTROL DE SESIÓN / ESTADO
    data.setdefault("open", True)

    return data





def backup_data():
    # Crear respaldo local de datos.json
    if os.path.exists("datos.json"):
        if not os.path.exists("respaldos"):
            os.mkdir("respaldos")

        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shutil.copy("datos.json", f"respaldos/datos_{date_str}.json")


def reset_data():
    # Reiniciar datos en modo pruebas
    if not TEST_MODE:
        print(t("reset_blocked_prod"))
        return

    confirmation = input(t("reset_confirm")).lower()
    if confirmation != "si":
        print(t("operation_cancelled"))
        return

    initial_data = {
    "current_month": datetime.now().strftime("%Y-%m"),
    "open": True,
    "income": [],
    "expenses": [],
    "goals": [],
    "closures": [],
    "history": [],
    "adjustments": [],
    "savings": {
        "emergency": 0,
        "total": 0
    },
    "summary": {
        "tithe": 0,
        "my_payment": 0,
        "available_payment": 0,
        "debts": 0,
        "cexpenses": 0,
        "emergency_saving": 0,
        "general_saving": 0
    }
}


    save_data(initial_data)
    print(t("data_reset_ok"))


def register_income():
    data = load_data()

    if not data.get("open", True):
        print(t("period_closed"))
        return
    

    # --- INGRESO ---
    try:
        amount = float(input(t("enter_income_amount")))
        if amount <= 0:
            print(t("amount_must_be_positive"))
            return
    except ValueError:
        print(t("invalid_number"))
        return

    # --- VALIDACIÓN SI / NO (DEUDAS) ---
    while True:
        debts_resp = input(t("has_debts")).strip().lower()

        if debts_resp in ["si", "sí"]:
            has_debts = True
            break
        elif debts_resp == "no":
            has_debts = False
            break
        else:
            print(t("invalid_yes_no"))

    # --- VALIDACIÓN SI / NO (DIEZMO) ---
    while True:
        tithe_resp = input(t("pay_tithe")).strip().lower()

        if tithe_resp in ["si", "sí"]:
            pay_tithe = True
            break
        elif tithe_resp == "no":
            pay_tithe = False
            break
        else:
            print(t("invalid_yes_no"))


    # --- DISTRIBUCIÓN BASE ---
    distribution = calculator.distribute_income(
        amount,
        has_debts,
        pay_tithe
    )

    my_payment = distribution["my_payment"]

    # --- AHORRO AUTOMÁTICO DESDE MI PAGO ---
    emergency_saving = my_payment * 0.05
    general_saving = my_payment * 0.05

    distribution["emergency_saving"] = emergency_saving
    distribution["general_saving"] = general_saving
    distribution["available_payment"] = my_payment - (emergency_saving + general_saving)

    # --- GUARDAR INGRESO DETALLADO ---
    data["income"].append({
        "fecha": datetime.now().isoformat(),
        "amount": amount,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # --- ACTUALIZAR RESUMEN ---
    for key, value in distribution.items():
        if key in data["summary"]:
            data["summary"][key] += value

    save_data(data)

    # --- SALIDA CLARA EN CONSOLA ---
    print(t("income_distribution_title"))
    if pay_tithe and distribution["tithe"] > 0:
        print(t(f"tithe_label ${distribution['tithe']:,.0f}"))

    print(t(f"gross_payment_label ${my_payment:,.0f}"))

    if has_debts and "debts" in distribution:
        print(t(f"debts_label ${distribution['debts']:,.0f}"))

    print(t("auto_savings_title"))
    print(t(f"emergency_saving_label ${emergency_saving:,.0f}"))
    print(t(f"general_saving_label ${general_saving:,.0f}"))

    print(t(f"net_payment_label ${distribution['available_payment']:,.0f}"))
    print(t("expenses_label"), f"${distribution['expenses']:,.0f}")





#SE TRADUCE HASTA AQUI 1


def register_expense():
    data = load_data()

    if not data.get("open", True):
        print(t("period_closed"))
        return


    print(t("expense_categories_title"))

    for i, category in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"{i:<2} {t(category)}")


    try:
        option = int(input(t("select_category")))
        if option < 1 or option > len(EXPENSE_CATEGORIES):
            print(t("invalid_option"))
            return
        category = EXPENSE_CATEGORIES[option - 1]
    except ValueError:  
        print(t("must_enter_number"))
        return


    while True:
        try:
            amount = float(input(t("enter_expense_amount")))
            if amount <= 0:
                print(t("amount_must_be_positive"))
                continue
            break
        except ValueError:
            print(t("invalid_number"))

    
    data["expenses"].append({
    "categoria": category,
    "amount": amount
    })

    save_data(data)

    print(t("expense.saved").format(
    category=t(category),
    amount=amount
    ))





def create_goal():
    data = load_data()

    name = input(t("goal_name"))
    target_amount = float(input(t("goal_target_amount")))

    goal = {
        "name": name,
        "aim": target_amount,
        "saved": 0
    }

    data["goals"].append(goal)
    save_data(data)

    print(t("goal.created").format(name=name, target_amount=target_amount))


def contribute_goal():
    data = load_data()

    if not data["goals"]:
        print(t("no_goals"))
        return

    print(t("goals_title"))
    for i, goal in enumerate(data["goals"], start=1):
        print(t("goal.progress").format(index=i, name=goal["name"], saved=goal["saved"], target=goal["aim"]))


    try:
        option = int(input(t("select_goal")))
        if option < 1 or option > len(data["goals"]):
            print(t("option_out_of_range"))
            return
    except ValueError:
        print(t("must_enter_number"))
        return

    try:
        amount = float(input(t("contribution_amount")))
        if amount <= 0:
            print(t("amount_must_be_positive"))
            return
    except ValueError:
        print(t("invalid_amount"))
        return

    if amount > data["savings"]["total"]:
        print(t("insufficient_savings"))
        return

    index = option - 1
    data["savings"]["total"] -= amount
    data["goals"][index]["saved"] += amount

    save_data(data)
    print(t("contribution_success"))


def expense_chart():
    data = load_data()

    if not data["expenses"]:
        print(t("no_expenses"))
        return

    categories = {}
    for expense in data["expenses"]:
        cat = expense["categoria"]
        categories[cat] = categories.get(cat, 0) + expense["amount"]

    names = list(categories.keys())
    values = list(categories.values())

    plt.figure()
    plt.bar(names, values)
    plt.title("Gastos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("chart_amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def goals_chart():
    data = load_data()

    if not data["goals"]:
        print(t("no_goals_registered"))
        return

    names = [goal["name"] for goal in data["goals"]]
    percentages = [
        (goal["saved"] / goal["aim"]) * 100
        for goal in data["goals"]
    ]

    plt.figure()
    plt.bar(names, percentages)
    plt.title("Progreso de metas (%)")
    plt.ylabel("Porcentaje completado")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def financial_report():
    data = load_data()

    print(t("financial_report_title"))

    total_income = sum(i.get("amount", 0) for i in data.get("income", []))
    total_expenses = sum(e.get("amount", 0) for e in data.get("expenses", []))

    print(t(f"total_income ${total_income:,.0f}"))
    print(t(f"total_expenses  ${total_expenses:,.0f}"))

    balance = total_income - total_expenses
    print(f"{t('balance')} ${balance:,.0f}")

    print(t("savings_title"))

    emergency = data.get("summary", {}).get("emergency_saving", 0)
    print(t("emergency_savings").format(amount=emergency))

    general = data.get("summary", {}).get("general_saving", 0)
    print(t("general_savings").format(amount=general))


    total = data.get("summary", {}).get("total_saving", 0)
    print(t("total_savings").format(amount=total))



def check_month_close(data):
    current_month = datetime.now().strftime("%Y-%m")

    # Inicializaciones seguras
    if "current_month" not in data:
        data["current_month"] = current_month

    if "history" not in data:
        data["history"] = []

    if "summary" not in data:
        data["summary"] = {
            "tithe": 0,
            "my_payment": 0,
            "debts": 0,
            "expenses": 0,
            "emergency_saving": 0,
            "general_saving": 0,
            "available_payment": 0
        }

    saved_month = data["current_month"]

    # Si cambió el mes → cerrar mes anterior
    if saved_month != current_month:
        data["history"].append({
            "month": saved_month,
            "summary": copy.deepcopy(data["summary"])
        })

        # Reiniciar mes
        data["current_month"] = current_month
        data["summary"] = {
            "tithe": 0,
            "my_payment": 0,
            "debts": 0,
            "expenses": 0,
            "emergency_saving": 0,
            "general_saving": 0,
            "available_payment": 0
        }

        data["income"] = []
        data["expenses"] = []

        save_data(data)

        print(t("month_closed_auto"))


def register_adjustment():
    data = load_data()

    if not data.get("open", True):
        print(t("period_closed"))
        return

    description = input(t("adjustment_description"))
    amount = float(input(t("adjustment_amount")))

    data["adjustments"].append({
        "fecha": datetime.now().isoformat(),
        "descripcion": description,
        "amount": amount
    })

    data["summary"]["expenses"] += amount
    save_data(data)

    print(t("adjustment_saved"))


def view_history():
    data = load_data()

    print(t("history_title"))
    for month in data["history"]:
        print(t(f"history_month {month['month']}"))
        for key, value in month["summary"].items():
            print(t(f"{key}: ${value:,.0f}"))


def get_history():
    data = load_data()
    return data.get("history", [])


def register_income_from_ui(amount, has_debts, pay_tithe):
    data = load_data()

    # === Inicialización segura de estructura ===
    data.setdefault("open", True)
    data.setdefault("income", [])
    data.setdefault("expenses", [])
    data.setdefault("history", [])
    data.setdefault("summary", {})

    for key in [
        "chart_income",
        "expenses",
        "total_saving",
        "tithe",
        "debts",
        "my_payment",
        "emergency_saving",
        "general_saving",
        "available_payment"
    ]:
        data["summary"].setdefault(key, 0)

    # Si no está abierto, no hacer nada
    if not data.get("open", True):
        return None

    income = float(amount)

    # ─── Distribución base desde calculadora ───
    distribution = calculator.distribute_income(
        income,
        has_debts,
        pay_tithe
    )

    # ─── Mi pago (10% fijo) ───
    my_payment = distribution["my_payment"]

    # ─── Ahorros automáticos (salen SOLO de mi pago) ───
    emergency_saving = my_payment * 0.05
    general_saving = my_payment * 0.05
    total_saving = emergency_saving + general_saving

    distribution["emergency_saving"] = emergency_saving
    distribution["general_saving"] = general_saving
    distribution["total_saving"] = total_saving
    distribution["available_payment"] = my_payment - total_saving

    # ─── ✅ CORRECCIÓN CLAVE: GASTOS CORRECTOS ───
    tithe = distribution.get("tithe", 0)
    debts = distribution.get("debts", 0)

    expenses = income - tithe - debts - my_payment
    distribution["expenses"] = expenses

    # ─── Guardar ingreso ───
    data["income"].append({
        "fecha": datetime.now().isoformat(),
        "amount": income,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # ─── Actualizar resumen ───
    data["summary"]["chart_income"] += income
    data["summary"]["tithe"] += tithe
    data["summary"]["debts"] += debts
    data["summary"]["expenses"] += expenses
    data["summary"]["my_payment"] += my_payment
    data["summary"]["emergency_saving"] += emergency_saving
    data["summary"]["general_saving"] += general_saving

    data["summary"]["total_saving"] = (
        data["summary"]["emergency_saving"] +
        data["summary"]["general_saving"]
    )

    data["summary"]["available_payment"] = (
        data["summary"]["my_payment"] -
        data["summary"]["total_saving"]
    )

    save_data(data)
    return distribution


def register_expense_from_ui(amount, category):
    data = load_data()

    if not data.get("open", True):
        print(t("period_closed"))
        return

    data["expenses"].append({
        "amount": amount,
        "categoria": category
    })

    data["summary"]["expenses"] -= amount

    save_data(data)
    return True





#SE TRADUCE HASTA AQUI 2

def get_monthly_report():
    data = load_data()
    summary = data.get("summary", {})

    report = {
        "tithe": summary.get("tithe", 0),
        "debts": summary.get("debts", 0),
        "expenses": summary.get("expenses", 0),
        "my_payment": summary.get("my_payment", 0),
        "emergency_saving": summary.get("emergency_saving", 0),
        "general_saving": summary.get("general_saving", 0),
        "total_saving": summary.get("total_saving", 0),
        "available_payment": summary.get("available_payment", 0),
    }

    return report


def get_history():
    data = load_data()
    return data.get("history", [])


def monthly_comparison_chart():
    history = get_history()

    if len(history) < 1:
        print(t("not_enough_months_to_compare"))
        return False

    months = []
    incomes = []
    expenses = []
    savings = []

    for month in history:
        summary = month["summary"]

        months.append(month["month"])
        incomes.append(
            summary.get("my_payment", 0) +
            summary.get("tithe", 0) +
            summary.get("debts", 0)
        )
        expenses.append(summary.get("expenses", 0))
        savings.append(
            summary.get("emergency_saving", 0) +
            summary.get("general_saving", 0)
        )

    plt.figure()
    plt.plot(months, incomes, label="chart_income")
    plt.plot(months, expenses, label="expenses")
    plt.plot(months, savings, label="chart_savings")

    plt.title("chart_monthly_comparison_title")
    plt.xlabel("chart_month")
    plt.ylabel("chart_amount")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return True


def compare_months(month1, month2):
    history = get_history()

    m1 = next((m for m in history if m["month"] == month1), None)
    m2 = next((m for m in history if m["month"] == month2), None)

    if not m1 or not m2:
        return None

    comparison = {}

    for key in m1["summary"]:
        comparison[key] = m2["summary"].get(key, 0) - m1["summary"].get(key, 0)

    return comparison


def get_month_status():
    data = load_data()
    return data.get("open", True)


def export_history_csv(path="financial_history.csv"):
    data = load_data()
    history = data.get("history", [])

    if not history:
        return False

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["chart_month", "Concepto", "chart_amount"])

        for month in history:
            for key, value in month["summary"].items():
                writer.writerow([month["month"], key, value])

    return True


def financial_analysis():
    data = load_data()
    history = data.get("history", [])

    if len(history) < 2:
        return "analysis_not_enough_data"

    current = history[-1]["summary"]
    previous = history[-2]["summary"]

    messages = []

    if current.get("expenses", 0) > previous.get("expenses", 0):
        messages.append("analysis_higher_expenses")

    if current.get("total_saving", 0) < previous.get("total_saving", 0):
        messages.append("analysis_savings_decreased")

    if not messages:
        messages.append("analysis_good_progress")

    return "\n".join(messages)


def main_menu():
    data = load_data()
    check_month_close(data)

    while True:

        mode = "🧪 PRUEBAS" if TEST_MODE else "🔒 PRODUCCIÓN"
        print(t("app_title_with_mode").format(mode=mode))

        print(t("menu_register_income"))
        print(t("menu_register_expense"))
        print(t("menu_create_goal"))
        print(t("menu_contribute_goal"))
        print(t("menu_view_report"))
        print(t("menu_expense_chart"))
        print(t("menu_goals_chart"))
        print(t("menu_reset_data"))
        print(t("menu_exit"))

        option = input(t("select_option") + "\n")

        if option == "1":
            register_income()

        elif option == "2":
            register_expense()

        elif option == "3":
            create_goal()

        elif option == "4":
            contribute_goal()

        elif option == "5":
            financial_report()

        elif option == "6":
            expense_chart()

        elif option == "7":
            goals_chart()

        elif option == "8":
            reset_data()

        elif option == "9":
            print(t("goodbye_message"))
            break

        else:
            print(t("invalid_option"))


def get_history_for_chart():
    data = load_data()
    return data.get("history", [])


def analyze_alerts():
    data = load_data()
    alerts = []

    summary = data.get("summary", {})
    income = summary.get("my_payment", 0)
    expenses = summary.get("expenses", 0)
    total_saving = summary.get("total_saving", 0)

    if income > 0:
        if expenses > income * rules.RULES["max_expense_pct"]:
            alerts.append("alert_high_expenses")

        if total_saving < income * rules.RULES["min_saving_pct"]:
            alerts.append("alert_low_savings")

    # Comparación ocio
    history = data.get("history", [])
    if len(history) >= 1:
        prev_month = history[-1]["summary"]
        prev_leisure = prev_month.get("Ocio", 0)
        current_leisure = 0  # si luego separas por categoría
        if prev_leisure > 0 and current_leisure > prev_leisure * (1 + rules.RULES["alerta_ocio_pct"]):
            alerts.append("alert_leisure_increase")

    return alerts


if __name__ == "__main__":
    run()

