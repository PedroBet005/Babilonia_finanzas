
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
    data["summary"].setdefault("tithe_label", 0)
    data["summary"].setdefault("debts_label", 0)
    data["summary"].setdefault("savings_babylon_label", 0)
    data["summary"].setdefault("expenses_label", 0)

    # 🔒 CONTROL DE SESIÓN / ESTADO
    data.setdefault("open", True)

    return data





def backup_data():
    # Crear respaldo local de datos.json
    if os.path.exists("datos.json"):
        if not os.path.exists("backups_label"):
            os.mkdir("backups_label")

        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shutil.copy("datos.json", f"backups_label/datos_{date_str}.json")


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
        "summary": {
            "tithe": 0,
            "debts": 0,
            "savings": 0,
            "expenses": 0,
            "chart_income": 0
        }
    }

    save_data(initial_data)
    print(t("data_reset_ok"))




#SE TRADUCE HASTA AQUI 1


def register_expense():
    data = load_data()

    if not data.get("open", True):
        print(t("period_closed"))
        return

    # --- Mostrar categorías traducidas ---
    print(t("expense_categories_title"))
    for i, category_key in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"{i:<2} {t(category_key)}")

    try:
        option = int(input(t("select_category")))
        if option < 1 or option > len(EXPENSE_CATEGORIES):
            print(t("invalid_option"))
            return
        category = EXPENSE_CATEGORIES[option - 1]
    except ValueError:
        print(t("must_enter_number"))
        return

    # --- Ingreso de monto ---
    while True:
        try:
            amount = float(input(t("enter_expense_amount")))
            if amount <= 0:
                print(t("amount_must_be_positive"))
                continue
            break
        except ValueError:
            print(t("invalid_number"))

    # --- Educa sin castigar: bloquear deudas de consumo ---
    if category == "category_debts":
        print(t("alert_no_new_debts"))
        print(t("educational_tip_debts"))
        return  # No se registra gasto de deuda de consumo

    data.setdefault("expenses", [])
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
    summary = data.get("summary", {})

    print(t("financial_report_title"))

    # ✅ El ingreso real debe venir de "income", no de "chart_income"
    total_income = summary.get("income", 0)

    print(f"{t('total_income_label')} ${total_income:,.0f}")
    print("")

    tithe = summary.get("tithe", 0)
    debts = summary.get("debts", 0)
    savings = summary.get("savings", 0)
    expenses = summary.get("expenses", 0)

    print(f"{t('tithe_label')} ${tithe:,.0f}")
    print(f"{t('debts_label')} ${debts:,.0f}")
    print(f"{t('savings_babylon_label')} ${savings:,.0f}")
    print(f"{t('expenses_label')} ${expenses:,.0f}")

    print("")

    balance = total_income - (tithe + debts + savings + expenses)

    print(f"{t('balance_label')} ${balance:,.0f}")




def check_month_close(data):
    current_month = datetime.now().strftime("%Y-%m")

    # Inicializaciones seguras
    if "current_month" not in data:
        data["current_month"] = current_month

    if "history" not in data:
        data["history"] = []

    if "summary" not in data:
        data["summary"] = {
            "tithe_label": 0,
            "debts_label": 0,
            "savings_babylon_label": 0,
            "expenses_label": 0,
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
            "debts": 0,
            "Savings (Babylon rule – 10%):": 0,
            "expenses": 0,
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


def register_income_from_ui():
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

    # --- ¿TIENE DEUDAS? ---
    while True:
        resp = input(t("has_debts")).strip().lower()
        if resp in ["si", "sí"]:
            has_debts = True
            break
        elif resp == "no":
            has_debts = False
            break
        else:
            print(t("invalid_yes_no"))

    # --- ¿PAGA DIEZMO? ---
    while True:
        resp = input(t("pay_tithe")).strip().lower()
        if resp in ["si", "sí"]:
            pay_tithe = True
            break
        elif resp == "no":
            pay_tithe = False
            break
        else:
            print(t("invalid_yes_no"))

    # --- DISTRIBUCIÓN DE INGRESO ---
    distribution = calculator.distribute_income(
        amount,
        has_debts,
        pay_tithe
    )

    # --- MOSTRAR DISTRIBUCIÓN EDUCATIVA ---
    print(t("distribution_title"))
    if pay_tithe and distribution["tithe"] > 0:
        print(f"{t('tithe_label')} ${distribution['tithe']:,.0f}")
    if has_debts and distribution["debts"] > 0:
        print(f"{t('debts_label')} ${distribution['debts']:,.0f}")
    print(f"{t('savings_babylon_label')} ${distribution['savings']:,.0f}")
    print(f"{t('expenses_label')} ${distribution['expenses']:,.0f}")

    # --- GUARDAR INGRESO ---
    data.setdefault("income", [])
    data.setdefault("summary", {
        "income": 0,
        "tithe": 0,
        "debts": 0,
        "savings": 0,
        "expenses": 0
    })

    data["income"].append({
        "fecha": datetime.now().isoformat(),
        "amount": amount,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # --- ACTUALIZAR RESUMEN ---
    data["summary"]["income"] += amount
    data["summary"]["tithe"] += distribution["tithe"]
    data["summary"]["debts"] += distribution["debts"]
    data["summary"]["savings"] += distribution["savings"]
    data["summary"]["expenses"] += distribution["expenses"]

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
        "Savings (Babylon rule – 10%)": summary.get("Savings (Babylon rule – 10%)", 0),
        "expenses": summary.get("expenses", 0),

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
    tithe = []
    debts = []
    savings = []
    expenses = []

    for month in history:
        summary = month.get("summary", {})

        months.append(month.get("month", ""))
        tithe.append(summary.get("tithe", 0))
        debts.append(summary.get("debts", 0))
        savings.append(summary.get("savings", 0))
        expenses.append(summary.get("expenses", 0))

    plt.figure()
    plt.plot(months, tithe, label=t("tithe_label"))
    plt.plot(months, debts, label=t("debts_label"))
    plt.plot(months, savings, label=t("savings_babylon_label"))
    plt.plot(months, expenses, label=t("expenses_label"))

    plt.title(t("chart_monthly_comparison_title"))
    plt.xlabel(t("chart_month"))
    plt.ylabel(t("chart_amount"))
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

    current = history[-1].get("summary", {})
    previous = history[-2].get("summary", {})

    messages = []

    # 📈 Gastos aumentaron
    if current.get("expenses", 0) > previous.get("expenses", 0):
        messages.append("analysis_higher_expenses")

    # 💰 Ahorro Babilonia disminuyó
    if current.get("savings", 0) < previous.get("savings", 0):
        messages.append("analysis_savings_decreased")

    # ✅ Buen progreso
    if not messages:
        messages.append("analysis_good_progress")

    return "\n".join(messages)



def distribute_income(amount, has_debts, pay_tithe, savings_pct=0.10):
    MIN_SAVINGS_PCT = 0.10
    DEBTS_PCT = 0.10
    TITHE_PCT = 0.10

    # 🔐 Validación Babilonia
    if savings_pct < MIN_SAVINGS_PCT:
        savings_pct = MIN_SAVINGS_PCT

    distribution = {}

    distribution["tithe"] = amount * TITHE_PCT if pay_tithe else 0
    distribution["savings"] = amount * savings_pct
    distribution["debts"] = amount * DEBTS_PCT if has_debts else 0

    distribution["expenses"] = max(
        0,
        amount - (
            distribution["tithe"] +
            distribution["savings"] +
            distribution["debts"]
        )
    )

    return distribution




def main_menu():
    data = load_data()
    check_month_close(data)

    while True:

        mode = "🧪 PRUEBAS" if TEST_MODE else "🔒 PRODUCCIÓN"
        print(t("app_title_with_mode").format(mode=mode))

        print(t("menu_register_income_from_ui"))
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
            register_income_from_ui()

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

    total_income = summary.get("chart_income", 0)
    expenses = summary.get("expenses", 0)
    savings = summary.get("savings", 0)

    if total_income <= 0:
        return alerts

    # 🔴 Alerta: gastos demasiado altos respecto al ingreso
    if expenses > total_income * rules.RULES["max_expense_pct"]:
        alerts.append("alert_high_expenses")

    # 🔴 Alerta: no se cumple la regla de Babilonia (10%)
    if savings < total_income * rules.RULES["min_saving_pct"]:
        alerts.append("alert_low_savings")

    # ⚠️ Comparación ocio (opcional, se mantiene)
    history = data.get("history", [])
    if len(history) >= 1:
        prev_month = history[-1].get("summary", {})
        prev_leisure = prev_month.get("Ocio", 0)
        current_leisure = 0  # pendiente si luego separas por categoría

        if (
            prev_leisure > 0 and
            current_leisure > prev_leisure * (1 + rules.RULES["alerta_ocio_pct"])
        ):
            alerts.append("alert_leisure_increase")

    return alerts



if __name__ == "__main__":
    run()

