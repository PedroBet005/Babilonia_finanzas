
import security as security
import calculator as calculator
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
import copy
import csv
import shutil
import os
import json
import rules
from i18n import t
import sys
from interfaz import init_app, show_menu, handle_change_language



def get_app_dir():
    try:
        base = os.environ.get("APPDATA")
        if not base:
            base = os.path.expanduser("~")
        path = os.path.join(base, "BabiloniaFinanzas")
        os.makedirs(path, exist_ok=True)
        return path
    except Exception as e:
        print("ERROR creando APP_DIR:", e)
        return os.getcwd()

APP_DIR = get_app_dir()



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # cuando es .exe
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

APP_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()

DATA_PATH = os.path.join(APP_DIR, "datos.json")
LOG_PATH = os.path.join(APP_DIR, "log.txt")

LOG_PATH


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



# ==============================
# CONFIGURACIÓN GENERAL 
# ==============================
TEST_MODE = False  # 🔁 Cambiar a False cuando uses datos reales



EXPENSE_CATEGORIES = [
    "food",                    # Alimentación
    "children",                # Hijas
    "fuel",                    # Combustible
    "vehicle",                 # Vehículo
    "utilities",               # Servicios públicos
    "operational_expenses",    # Gastos operativos
    "productive_project",      # Proyecto productivo
    "social_contributions",    # Aportes sociales
    "agreements",              # Convenios
    "leisure",                 # Ocio
    "other"                    # Otros
]





def normalize_expense_categories():
    data = load_data()
    expenses = data.get("expenses", [])

    mapping = {
        "transport": "fuel",        # o utilities según tu lógica
        "food": "food",
        "other": "other"
    }

    for e in expenses:
        cat = e.get("category")
        if isinstance(cat, str):
            cat = cat.lower().replace("category_", "")
            if cat in mapping:
                e["category"] = mapping[cat]

    save_data(data)



def calculate_balance(data):
    total_budget_expenses = 0

    for income in data.get("income", []):
        dist = income.get("distribucion", {})
        total_budget_expenses += dist.get("expenses", 0)

    total_spent = sum(e.get("amount", 0) for e in data.get("expenses", []))
    available = total_budget_expenses - total_spent

    return available, total_budget_expenses, total_spent




def save_data(data):
    try:
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"save_ok - {datetime.now().isoformat()}\n")

    except Exception as e:
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as log:
                log.write(f"save_error - {datetime.now().isoformat()} - {e}\n")
        finally:
            raise



def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # --- ESTRUCTURA BASE ---
    if "summary" not in data:
        data["summary"] = {}

    data["summary"].setdefault("tithe", 0)
    data["summary"].setdefault("debts", 0)
    data["summary"].setdefault("savings", 0)
    data["summary"].setdefault("expenses", 0)

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
            "income": 0,
            "tithe": 0,
            "debts": 0,
            "savings": 0,
            "expenses": 0,
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

    balance, _, _ = calculate_balance(data)

    # === Entrada de datos ===
    expense_name = input("Nombre del gasto: ").strip()
    category = input("Categoría del gasto: ").strip()

    try:
        amount = float(input("Monto del gasto: "))
    except ValueError:
        print("Monto inválido")
        return

    if amount <= 0:
        print("El monto debe ser mayor a cero")
        return

    if amount > balance:
        print("Saldo insuficiente")
        return

    # === Registrar gasto ===
    data.setdefault("expenses", [])

    data["expenses"].append({
        "fecha": datetime.now().isoformat(),
        "category": category,
        "amount": amount,
        "name": expense_name
    })

    save_data(data)
    print(t("expense_saved"))



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

    income = data.get("income", [])
    expenses = data.get("expenses", [])

    total_income = sum(i.get("amount", 0) for i in income)

    tithe = sum(i["distribucion"].get("tithe", 0) for i in income)
    debts = sum(i["distribucion"].get("debts", 0) for i in income)
    savings = sum(i["distribucion"].get("savings", 0) for i in income)

    spent = sum(e.get("amount", 0) for e in expenses)

    available, budget, _ = calculate_balance(data)

    print(t("financial_report_title"))
    print(f"{t('tithe_label')} ${tithe:,.0f}")
    print(f"{t('debts_label')} ${debts:,.0f}")
    print(f"{t('savings_babylon_label')} ${savings:,.0f}")
    print(f"{t('expenses_label')} ${spent:,.0f}")
    print(f"{t('balance_label')} ${available:,.0f}")





def list_expenses():
    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        print(t("no_expenses"))
        return

    print(t("expenses_title"))

    for expense in expenses:
        amount = expense.get("amount", 0)
        name = expense.get("name")

        raw_category = expense.get("category") or expense.get("categoria")
        label = None

        # 1️⃣ Nombre personalizado (Otros)
        if name:
            label = name

        # 2️⃣ Categoría
        elif isinstance(raw_category, str):
            category = raw_category.strip().lower()

            # limpiar prefijos viejos
            if category.startswith("category_"):
                category = category.replace("category_", "")

            # intentar traducción
            key = "category_" + category
            translated = t(key)

            # si no existe traducción → NO mostrar inglés
            if translated != key:
                label = translated
            else:
                label = t("category_other")

        # 3️⃣ Respaldo final
        if not label:
            label = t("category_other")

        print(f"- {label}: ${amount:,.0f}")



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

    data.setdefault("expenses", [])

    data["expenses"].append({
        "fecha": datetime.now().isoformat(),
        "category": "adjustment",
        "name": description,
        "amount": amount
    })

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

def log_error(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def register_income(amount: float, has_debts: bool, pay_tithe: bool):
    data = load_data()

    if not data.get("open", True):
        raise RuntimeError("period_closed")

    if amount <= 0:
        raise ValueError("amount_must_be_positive")

    distribution = calculator.distribute_income(
        amount,
        has_debts,
        pay_tithe
    )

    # 🔑 Claves CONSISTENTES
    data.setdefault("incomes", [])
    data.setdefault("summary", {
        "income": 0,
        "tithe": 0,
        "debts": 0,
        "savings": 0,
        "expenses": 0
    })

    data["incomes"].append({
        "fecha": datetime.now().isoformat(),
        "amount": amount,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # ✅ actualizar resumen
    data["summary"]["income"] += amount
    data["summary"]["tithe"] += distribution.get("tithe", 0)
    data["summary"]["debts"] += distribution.get("debts", 0)
    data["summary"]["savings"] += distribution.get("savings", 0)

    # 🔐 GUARDADO SEGURO (clave para .exe)
    try:
        save_data(data)
    except Exception as e:
        log_error(str(e))
        raise RuntimeError("error_saving")

    return distribution




def register_income_from_ui(amount, has_debts, pay_tithe):
    data = load_data()

    if not data.get("open", True):
        raise Exception(t("period_closed"))

    amount = float(amount)
    if amount <= 0:
        raise Exception(t("amount_must_be_positive"))

    distribution = calculator.distribute_income(
        amount,
        has_debts,
        pay_tithe
    )

    data.setdefault("income", [])

    data["income"].append({
        "fecha": datetime.now().isoformat(),
        "amount": amount,
        "tiene_deudas": has_debts,
        "paga_diezmo": pay_tithe,
        "distribucion": distribution
    })

    save_data(data)
    return distribution





def register_expense_from_ui(amount, category):
    data = load_data()

    if not data.get("open", True):
        return False

    data.setdefault("expenses", [])

    data["expenses"].append({
        "fecha": datetime.now().isoformat(),
        "amount": amount,
        "category": category
    })

    save_data(data)
    return True





#SE TRADUCE HASTA AQUI 2

def get_monthly_report():
    data = load_data()

    available, budget, spent = calculate_balance(data)

    summary = {
        "Diezmo": sum(i["distribucion"].get("tithe", 0) for i in data["income"]),
        "Mi pago": sum(i["distribucion"].get("savings", 0) for i in data["income"]),
        "Mi pago disponible": sum(i["distribucion"].get("expenses", 0) for i in data["income"]),
        "Ahorro emergencia": 0,
        "Ahorro general": sum(i["distribucion"].get("savings", 0) for i in data["income"]),
        "Ahorro total": sum(i["distribucion"].get("savings", 0) for i in data["income"]),
        "Deudas": sum(i["distribucion"].get("debts", 0) for i in data["income"]),
        "Gastos": spent
    }

    return summary



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
    # 1️⃣ Cargar datos al iniciar la app
    data = load_data()


    # 3️⃣ Validar cierre de mes / periodo
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

        option = input(t("select_option") + "\n").strip()

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
            print("")  # separación visual
            list_expenses()

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




#def registrar_ingreso_desde_ui(amount, has_debt, pays_tithe):
    """
    Función exclusiva para la interfaz gráfica.
    No usa input(), no imprime, solo procesa.
    """

 #   data = load_data()

    # ⛔ Bloqueo si el mes está cerrado
#   if not data.get("open", True):
#       return None
#
#   distribution = {}

    # Diezmo (si aplica)


#    def safe_number(value):
#       return value if isinstance(value, (int, float)) else 0

#    tithe = 0
#    if pays_tithe:
#        tithe = round(amount * 0.10)
#       data["tithe"] = safe_number(data.get("tithe")) + tithe

    # Ahorro (regla Babilonia)
#    saving = round(amount * 0.10)
#   data["savings"] = safe_number(data.get("savings")) + saving

    # Deudas
#    debts = 0
#    if has_debt:
#        debts = round(amount * 0.20)
#       data["debts"] = safe_number(data.get("debts")) + debts

# Gastos
#    expenses = amount - tithe - saving - debts
#   data["expenses"] = safe_number(data.get("expenses")) + expenses

#   save_data(data)

# Resultado para mostrar en la UI
#    distribution["Diezmo"] = tithe
#   distribution["Ahorro"] = saving
#  distribution["Deudas"] = debts
# distribution["Gastos"] = expenses

#    return distribution


def registrar_gasto_desde_ui(amount, category):
    data = load_data()

    if not data.get("open", True):
        return False

    amount = float(amount)
    if amount <= 0:
        return False

    # 🔑 calcular saldo REAL
    available, _, _ = calculate_balance(data)

    if amount > available:
        return False

    # registrar gasto
    data.setdefault("expenses", [])
    data["expenses"].append({
        "fecha": datetime.now().isoformat(),
        "category": category,
        "amount": amount
    })

    save_data(data)
    return True





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



# ===============================
# PUENTES PARA HERRAMIENTAS GUI
# ===============================

def obtener_historial():
    """Historial general de ingresos y gastos"""
    data = load_data()
    return {
        "income": data.get("income", []),
        "expenses": data.get("expenses", [])
    }


def obtener_historial_para_grafica():
    """Historial preparado para gráficas"""
    return obtener_historial()


def analizar_alertas():
    """Alias en español para la interfaz"""
    return analyze_alerts()


def exportar_historial_csv():
    """Exporta historial a CSV"""
    return export_history_csv()


def analisis_financiero():
    """Análisis financiero simple en texto"""
    data = load_data()
    summary = data.get("summary", {})

    messages = []

    if summary.get("expenses", 0) > summary.get("income", 0) * 0.6:
        messages.append("⚠️ Tus gastos superan el 60% de tus ingresos.")

    if summary.get("savings", 0) <= 0:
        messages.append("⚠️ No estás ahorrando. Babilonia recomienda mínimo 10%.")

    if summary.get("debts", 0) > 0:
        messages.append("📌 Prioriza pagar tus deudas y evita nuevas.")

    if not messages:
        messages.append("✅ Tus finanzas están equilibradas. Buen trabajo.")

    return "\n".join(messages)


def print_financial_summary(diezmo, deudas, ahorro, disponible):
    print("\n📊 RESUMEN FINANCIERO BABILÓNICO\n")

    print(f"🙏 Diezmo: {diezmo}")
    print(f"🧾 Deudas: {deudas}")
    print(f"🏦 Ahorro (regla de Babilonia – 10%): {ahorro}")
    print("---------------------------------------")
    print(f"💰 Gasto disponible: {disponible}\n")


# ==============================
# ALIAS PARA LA INTERFAZ GRÁFICA
# ==============================

def grafica_comparacion_mensual():
    """
    Alias para compatibilidad con interfaz.py
    """
    return monthly_comparison_chart()




def main():
    handle_change_language()   # 🌍 Idioma al iniciar
    init_app()
    show_menu()

if __name__ == "__main__":
    main()




