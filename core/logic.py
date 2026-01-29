# logic.py
import os
import json
from datetime import datetime
from local.lang import t   # luego puedes hacerlo dinámico



DATA_PATH = os.path.join(os.getcwd(), "datos.json")
LOG_PATH = os.path.join(os.getcwd(), "log.txt")


def log_error(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def load_data():
    if not os.path.exists(DATA_PATH):
        return {
            "incomes": [],
            "expenses": [],
            "summary": {
                "income": 0,
                "tithe": 0,
                "debts": 0,
                "savings": 0,
                "expenses": 0
            },
            "open": True
        }

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ✅ FUNCIÓN QUE FALTABA
def register_income(amount, source="Ingreso", apply_tithe=False, apply_debt=False):
    data = load_data()

    if not data.get("open", True):
        return t("period_closed")

    if amount <= 0:
        return t("amount_must_be_positive")

    # Reglas babilónicas
    savings = round(amount * 0.10, 2)  # Siempre 10%
    tithe = round(amount * 0.10, 2) if apply_tithe else 0
    debts = round(amount * 0.10, 2) if apply_debt else 0

    available = round(amount - savings - tithe - debts, 2)

    income = {
        "date": datetime.now().isoformat(),
        "source": source,
        "amount": amount,
        "savings": savings,
        "tithe": tithe,
        "debts": debts
    }

    data.setdefault("incomes", []).append(income)

    data.setdefault("summary", {
        "income": 0,
        "savings": 0,
        "tithe": 0,
        "debts": 0
    })

    data["summary"]["income"] += amount
    data["summary"]["savings"] += savings
    data["summary"]["tithe"] += tithe
    data["summary"]["debts"] += debts

    save_data(data)

    # 👉 NUEVA SALIDA CONSOLIDADA Y ORDENADA
    return (
        f"{t('income_saved')}\n\n"
        f"{t('balance_title')}\n\n"
        f"🙏 {t('tithe')}: {tithe}\n"
        f"🧾 {t('debts')}: {debts}\n"
        f"🏦 {t('savings')}: {savings}\n"
        f"---------------------------------------\n"
        f"💰 {t('available')}: {available}"
    )




def calculate_balance(data):
    total_income = data["summary"].get("income", 0)
    total_expenses = data["summary"].get("expenses", 0)
    return total_income - total_expenses


def register_expense(amount, category):
    data = load_data()

    if not data.get("open", True):
        return t("period_closed")

    if amount <= 0:
        return t("amount_must_be_positive")

    expense = {
        "date": datetime.now().isoformat(),
        "category": category,
        "amount": amount
    }

    data.setdefault("expenses", []).append(expense)

    data["summary"]["expenses"] += amount

    save_data(data)
    return t("expense_saved")




def get_balance_report():
    data = load_data()

    total_income = data["summary"].get("income", 0)
    total_expenses = data["summary"].get("expenses", 0)
    total_savings = data["summary"].get("savings", 0)
    total_tithe = data["summary"].get("tithe", 0)
    total_debts = data["summary"].get("debts", 0)

    balance = (
        total_income
        - total_expenses
        - total_savings
        - total_tithe
        - total_debts
    )

    return {
        "income": total_income,
        "expenses": total_expenses,
        "savings": total_savings,
        "tithe": total_tithe,
        "debts": total_debts,
        "balance": balance
    }

