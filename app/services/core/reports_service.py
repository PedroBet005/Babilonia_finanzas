from datetime import datetime
import os

import matplotlib
matplotlib.use("Agg")  # 👈 CLAVE para .exe
import matplotlib.pyplot as plt

from app.services.core.logic import load_data
from app.services.local.lang import t



def export_financial_evolution_txt():
    data = load_data()
    movements = {}

    def parse_date(item):
        raw = item.get("fecha") or item.get("date")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except Exception:
            return None

    # --- Ingresos ---
    for item in data.get("incomes", []):
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["income"] += float(item.get("amount", 0))

    # --- Gastos ---
    for item in data.get("expenses", []):
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0.0, "expense": 0.0, "saving": 0.0})
        movements[key]["expense"] += float(item.get("amount", 0))

    if not movements:
        print("ℹ️", t("no_data"))
        return

    # --- Ahorro babilónico (10%) ---
    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    # --- Carpeta reportes ---
    folder = "reports"
    os.makedirs(folder, exist_ok=True)

    periods = sorted(movements.keys())
    filename = f"financial_evolution_{periods[0]}.txt"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("financial_evolution_title") + "\n")
            f.write("=" * 50 + "\n\n")

            if len(periods) > 1:
                f.write(t("multi_month_warning") + "\n\n")

            total_income = total_expense = total_saving = total_balance = 0.0

            for period in periods:
                year, month = period.split("-")
                month_label = f"{t('month_names')[int(month)]} {year}"

                income = movements[period]["income"]
                expense = movements[period]["expense"]
                saving = movements[period]["saving"]
                balance = income - expense - saving

                total_income += income
                total_expense += expense
                total_saving += saving
                total_balance += balance

                f.write(f"📅 {month_label}\n")
                f.write(f"  💰 {t('income')}: {income:.2f}\n")
                f.write(f"  📉 {t('expense')}: {expense:.2f}\n")
                f.write(f"  🏺 {t('savings')}: {saving:.2f}\n")
                f.write(f"  📊 {t('balance')}: {balance:.2f}\n")
                f.write("-" * 50 + "\n")

            # --- TOTAL GENERAL ---
            f.write("\n📌 " + t("grand_total") + "\n")
            f.write(f"💰 {t('income')}: {total_income:.2f}\n")
            f.write(f"📉 {t('expense')}: {total_expense:.2f}\n")
            f.write(f"🏺 {t('savings')}: {total_saving:.2f}\n")
            f.write(f"📊 {t('balance')}: {total_balance:.2f}\n")

        print(f"✅ {t('export_success')}: {filepath}")

    except Exception as e:
        print("❌", t("export_error"))
        print(e)





def export_expenses_by_category_txt():
    import os
    from datetime import datetime

    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        print("ℹ️", t("no_data"))
        return

    categories = {}
    months = set()

    def parse_date(item):
        raw = item.get("fecha") or item.get("date")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except Exception:
            return None

    # --- Procesar gastos ---
    for item in expenses:
        date = parse_date(item)
        if not date:
            continue

        month_key = f"{date.year}-{date.month:02d}"
        months.add(month_key)

        category = item.get("category", t("others"))
        amount = float(item.get("amount", 0))

        categories[category] = categories.get(category, 0) + amount

    if not categories:
        print("ℹ️", t("no_data"))
        return

    # --- Preparar carpeta ---
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # --- Nombre del mes ---

    if len(months) == 1:
        year, month = list(months)[0].split("-")
        month_label = f"{t('month_names')[int(month)]} {year}"
        filename = f"expenses_by_category_{year}-{month}.txt"
    else:
        month_label = t("multiple_periods")
        filename = "expenses_by_category_multiple_periods.txt"
        
        filepath = os.path.join(reports_dir, filename)

    # --- Exportar ---
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("expenses_by_category") + "\n")
            f.write(f"📅 {t('period')}: {month_label}\n")
            f.write("=" * 50 + "\n\n")

            grand_total = sum(categories.values())

            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percent = (amount / grand_total) * 100 if grand_total else 0
                f.write(f"{cat:<25} {amount:>10.2f}  ({percent:>5.1f}%)\n")

            f.write("\n" + "-" * 50 + "\n")
            f.write(f"{t('total')}: {grand_total:.2f}\n")

            if len(months) > 1:
                f.write("\n⚠️ " + t("multi_month_warning") + "\n")

        print(f"✅ {t('export_success')}: {filepath}")

    except Exception as e:
        print("❌", t("export_error"))
        print(e)





def build_financial_evolution(data):
    movements = {}

    def parse_date(item):
        raw = item.get("fecha") or item.get("date")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except Exception:
            return None

    for item in data.get("incomes", []):
        date = parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0, "expense": 0, "saving": 0})
        movements[key]["income"] += item.get("amount", 0)

    for item in data.get("expenses", []):
        date = parse_date(item)
        if not date:
            continue
        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0, "expense": 0, "saving": 0})
        movements[key]["expense"] += item.get("amount", 0)

    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    return movements



def export_babylon_savings_txt():
    import os
    from datetime import datetime

    data = load_data()
    incomes = data.get("incomes", [])

    if not incomes:
        print("ℹ️", t("no_data"))
        return

    savings = {}
    months = set()

    def parse_date(item):
        raw = item.get("fecha") or item.get("date")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except Exception:
            return None

    # --- Procesar ingresos ---
    for item in incomes:
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        months.add(key)

        amount = float(item.get("amount", 0))
        savings[key] = savings.get(key, 0) + (amount * 0.10)

    if not savings:
        print("ℹ️", t("no_data"))
        return

    # --- Preparar carpeta ---
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # --- Nombre del mes ---

    if len(months) == 1:
        year, month = list(months)[0].split("-")
        month_label = f"{t('month_names')[int(month)]} {year}"
        filename = f"babylonian_savings_{year}-{month}.txt"
    else:
        month_label = t("multiple_periods")
        filename = "babylonian_savings_multiple_periods.txt"

        filepath = os.path.join(reports_dir, filename)

    # --- Exportar ---
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(t("finance_title") + "\n")
            f.write(t("babylonian_savings") + "\n")
            f.write(f"📅 {t('period')}: {month_label}\n")
            f.write("=" * 50 + "\n\n")

            total_amount = 0.0

            for period in sorted(savings.keys()):
                year, month = period.split("-")
                month_name = f"{t('month_names')[int(month)]} {year}"
                amount = savings[period]
                total_amount += amount

                f.write(f"📅 {month_name}\n")
                f.write(f"   🏺 {t('savings')}: {amount:.2f}\n")
                f.write("-" * 40 + "\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"{t('total')}: {total_amount:.2f}\n")

            if len(months) > 1:
                f.write("\n⚠️ " + t("multi_month_warning") + "\n")

        print(f"✅ {t('export_success')}: {filepath}")

    except Exception as e:
        print("❌", t("export_error"))
        print(e)



def export_financial_evolution_chart():
    data = load_data()

    movements = {}

    def parse_date(item):
        raw = item.get("fecha") or item.get("date")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(raw)
        except Exception:
            return None

    # --- Ingresos ---
    for item in data.get("incomes", []):
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0, "expense": 0, "saving": 0})
        movements[key]["income"] += float(item.get("amount", 0))

    # --- Gastos ---
    for item in data.get("expenses", []):
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {"income": 0, "expense": 0, "saving": 0})
        movements[key]["expense"] += float(item.get("amount", 0))

    if not movements:
        print("ℹ️", t("no_data"))
        return

    # --- Ahorro babilónico ---
    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    # 📂 Carpeta reportes
    os.makedirs("reports", exist_ok=True)

    periods = sorted(movements.keys())
    incomes = [movements[p]["income"] for p in periods]
    expenses = [movements[p]["expense"] for p in periods]
    savings = [movements[p]["saving"] for p in periods]

    plt.figure(figsize=(10, 5))
    plt.plot(periods, incomes, marker="o", label=t("income"))
    plt.plot(periods, expenses, marker="o", label=t("expense"))
    plt.plot(periods, savings, marker="o", label=t("savings_label"))

    plt.title(t("chart_title"))
    plt.xlabel(t("period"))
    plt.ylabel(t("amount"))
    plt.grid(True)

    filename = "reports/financial_evolution.png"
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    print(f"📊 {t('chart_exported')}: {filename}")
