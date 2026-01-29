from datetime import datetime
from core.logic import load_data
from local.lang import t
import os


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
    folder = "reportes"
    os.makedirs(folder, exist_ok=True)

    periods = sorted(movements.keys())
    filename = f"evolucion_financiera_{periods[0]}.txt"
    filepath = os.path.join(folder, filename)

    month_names = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("🏛️ FINANZAS DE BABILONIA\n")
            f.write("📈 Evolución financiera del oro\n")
            f.write("=" * 50 + "\n\n")

            if len(periods) > 1:
                f.write("🧠 Aviso: El reporte contiene múltiples meses\n\n")

            total_income = total_expense = total_saving = total_balance = 0.0

            for period in periods:
                year, month = period.split("-")
                month_label = f"{month_names[int(month)]} {year}"

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
            f.write("\n📌 TOTAL GENERAL\n")
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
    reports_dir = "reportes"
    os.makedirs(reports_dir, exist_ok=True)

    # --- Nombre del mes ---
    month_names = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    if len(months) == 1:
        year, month = list(months)[0].split("-")
        month_label = f"{month_names[int(month)]} {year}"
        filename = f"gastos_por_categoria_{year}-{month}.txt"
    else:
        month_label = "Varios períodos"
        filename = "gastos_por_categoria_varios_periodos.txt"

    filepath = os.path.join(reports_dir, filename)

    # --- Exportar ---
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("🏛️ FINANZAS DE BABILONIA\n")
            f.write("📂 GASTOS POR CATEGORÍA\n")
            f.write(f"📅 Período: {month_label}\n")
            f.write("=" * 50 + "\n\n")

            total_general = sum(categories.values())

            for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percent = (amount / total_general) * 100 if total_general else 0
                f.write(f"{cat:<25} {amount:>10.2f}  ({percent:>5.1f}%)\n")

            f.write("\n" + "-" * 50 + "\n")
            f.write(f"{t('total')}: {total_general:.2f}\n")

            if len(months) > 1:
                f.write("\n⚠️ Aviso: Este reporte incluye más de un mes.\n")

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
    reports_dir = "reportes"
    os.makedirs(reports_dir, exist_ok=True)

    # --- Nombre del mes ---
    month_names = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    if len(months) == 1:
        year, month = list(months)[0].split("-")
        month_label = f"{month_names[int(month)]} {year}"
        filename = f"ahorro_babilonico_{year}-{month}.txt"
    else:
        month_label = "Varios períodos"
        filename = "ahorro_babilonico_varios_periodos.txt"

    filepath = os.path.join(reports_dir, filename)

    # --- Exportar ---
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("🏛️ FINANZAS DE BABILONIA\n")
            f.write("🏺 AHORRO BABILÓNICO (10%)\n")
            f.write(f"📅 Período: {month_label}\n")
            f.write("=" * 50 + "\n\n")

            total_general = 0.0

            for period in sorted(savings.keys()):
                year, month = period.split("-")
                month_name = f"{month_names[int(month)]} {year}"
                amount = savings[period]
                total_general += amount

                f.write(f"📅 {month_name}\n")
                f.write(f"   🏺 Ahorro: {amount:.2f}\n")
                f.write("-" * 40 + "\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write(f"{t('total')}: {total_general:.2f}\n")

            if len(months) > 1:
                f.write("\n⚠️ Aviso: Este reporte incluye más de un mes.\n")

        print(f"✅ {t('export_success')}: {filepath}")

    except Exception as e:
        print("❌", t("export_error"))
        print(e)
