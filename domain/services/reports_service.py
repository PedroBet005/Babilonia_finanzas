# reports_service.py
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.services.financie.logic import load_data
from app.local.lang import t
from app.services.storage.storage import load_data


# ==========================================================
# Output directory
# ==========================================================

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Helpers
# ==========================================================

def _parse_date(item):
    raw = item.get("fecha") or item.get("date")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except Exception:
        return None


def _no_data():
    return {"status": "no_data", "message_key": "no_data"}


# ==========================================================
# Financial evolution (TXT)
# ==========================================================

def export_financial_evolution_txt():
    data = load_data()
    movements = {}

    for item in data.get("incomes", []):
        date = _parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["income"] += float(item.get("amount", 0))

    for item in data.get("expenses", []):
        date = _parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["expense"] += float(item.get("amount", 0))

    if not movements:
        return _no_data()

    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    periods = sorted(movements.keys())
    filename = f"financial_evolution_{periods[0]}.txt"
    filepath = REPORTS_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("financial_evolution_title") + "\n")
            f.write("=" * 50 + "\n\n")

            for period in periods:
                year, month = period.split("-")
                label = f"{t('month_names')[int(month)]} {year}"

                income = movements[period]["income"]
                expense = movements[period]["expense"]
                saving = movements[period]["saving"]
                balance = income - expense - saving

                f.write(f"📅 {label}\n")
                f.write(f"  💰 {t('income')}: {income:.2f}\n")
                f.write(f"  📉 {t('expense')}: {expense:.2f}\n")
                f.write(f"  🏺 {t('savings')}: {saving:.2f}\n")
                f.write(f"  📊 {t('balance')}: {balance:.2f}\n")
                f.write("-" * 50 + "\n")

        return {"status": "ok", "file": str(filepath)}

    except Exception as e:
        return {"status": "error", "error": str(e)}


# ==========================================================
# Expenses by category (TXT)
# ==========================================================

def export_expenses_by_category_txt():
    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        return _no_data()

    categories = {}

    for item in expenses:
        date = _parse_date(item)
        if not date:
            continue

        category = item.get("category", t("others"))
        categories[category] = categories.get(category, 0) + float(item.get("amount", 0))

    if not categories:
        return _no_data()

    filename = "expenses_by_category.txt"
    filepath = REPORTS_DIR / filename

    try:
        total = sum(categories.values())

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("expenses_by_category") + "\n")
            f.write("=" * 50 + "\n\n")

            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percent = (amount / total) * 100 if total else 0
                f.write(f"{cat:<25} {amount:>10.2f} ({percent:>5.1f}%)\n")

            f.write("\n" + "-" * 50 + "\n")
            f.write(f"{t('total')}: {total:.2f}\n")

        return {"status": "ok", "file": str(filepath)}

    except Exception as e:
        return {"status": "error", "error": str(e)}


# ==========================================================
# Babylonian savings (TXT)
# ==========================================================

def export_babylon_savings_txt():
    data = load_data()
    incomes = data.get("incomes", [])

    if not incomes:
        return _no_data()

    savings = {}

    for item in incomes:
        date = _parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        savings[key] = savings.get(key, 0) + float(item.get("amount", 0)) * 0.10

    if not savings:
        return _no_data()

    filename = "babylonian_savings.txt"
    filepath = REPORTS_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("babylonian_savings") + "\n")
            f.write("=" * 50 + "\n\n")

            total = 0.0
            for period in sorted(savings.keys()):
                year, month = period.split("-")
                label = f"{t('month_names')[int(month)]} {year}"
                amount = savings[period]
                total += amount

                f.write(f"📅 {label}\n")
                f.write(f"   🏺 {t('savings')}: {amount:.2f}\n")
                f.write("-" * 40 + "\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"{t('total')}: {total:.2f}\n")

        return {"status": "ok", "file": str(filepath)}

    except Exception as e:
        return {"status": "error", "error": str(e)}


# ==========================================================
# Financial evolution (Chart)
# ==========================================================

def export_financial_evolution_chart():
    data = load_data()
    movements = {}

    for item in data.get("incomes", []):
        date = _parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["income"] += float(item.get("amount", 0))

    for item in data.get("expenses", []):
        date = _parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["expense"] += float(item.get("amount", 0))

    if not movements:
        return _no_data()

    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    periods = sorted(movements.keys())
    incomes = [movements[p]["income"] for p in periods]
    expenses = [movements[p]["expense"] for p in periods]
    savings = [movements[p]["saving"] for p in periods]

    plt.figure(figsize=(10, 5))
    plt.plot(periods, incomes, marker="o", label=t("income"))
    plt.plot(periods, expenses, marker="o", label=t("expense"))
    plt.plot(periods, savings, marker="o", label=t("savings"))

    plt.title(t("chart_title"))
    plt.xlabel(t("period"))
    plt.ylabel(t("amount"))
    plt.grid(True)

    filepath = REPORTS_DIR / "financial_evolution.png"
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return {"status": "ok", "file": str(filepath)}
