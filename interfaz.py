
from local.lang import t, set_language
from core.logic import register_income, register_expense
from core.logic import load_data, save_data
from datetime import datetime
from core.reports import (
    export_financial_evolution_txt,
    export_expenses_by_category_txt,
    export_babylon_savings_txt
)




def print_financial_summary(diezmo, deudas, ahorro, disponible):
    print("\n" + t("balance_title"))
    print()
    print(f"{t('tithe')}: {diezmo}")
    print(f"{t('debts')}: {deudas}")
    print(f"{t('savings')}: {ahorro}")
    print("---------------------------------------")
    print(f"{t('available')}: {disponible}")



def init_app():
    # Inicialización general de la app
    # ❌ NO preguntar idioma aquí
    pass



def handle_change_language():
    print("\n🌍 Idioma / Language")
    print("1️⃣ Español")
    print("2️⃣ English")

    choice = input("👉 ").strip()

    if choice == "1":
        set_language("es")
    elif choice == "2":
        set_language("en")

    print(t("welcome"))



def show_menu():    
    while True:
        print("\n📜", t("main_menu"))
        print("1️⃣ ", t("menu_income"))
        print("2️⃣ ", t("menu_expense"))
        print("3️⃣ ", t("menu_balance"))
        print("4️⃣ ", t("menu_change_language"))
        print("5️⃣ 🧾", t("financial_tools"))
        print("6️⃣ ", t("exit"))

        option = input("👉 " + t("select_option") + ": ")

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




def handle_register_income():
    amount = float(input(t("enter_amount")))
    source = input(t("enter_source"))

    apply_tithe = input("🙏 ¿Aplicar diezmo? (s/n): ").lower() == "s"
    apply_debt = input("🧾 ¿Aplicar deudas? (s/n): ").lower() == "s"

    result = register_income(
        amount,
        source,
        apply_tithe=apply_tithe,
        apply_debt=apply_debt
    )

    print(result)




def handle_register_expense():
    data = load_data()

    print("\n➖ REGISTRAR GASTO")

    categories = [
        "Alimentación",
        "Hijos(as)",
        "Aportes sociales",
        "Combustible",
        "Vehículo",
        "Servicios públicos",
        "Operativos",
        "Proyecto productivo",
        "Ocio",
        "Otros"
    ]

    print("\n📂 Categoría del gasto:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    try:
        choice = int(input("👉 Selecciona una opción: "))
        category = categories[choice - 1]
    except (ValueError, IndexError):
        print("❌ Opción inválida")
        return

    if category == "Otros":
        category = input("✏️ Nombre del gasto: ")

    try:
        amount = float(input("💸 Monto del gasto: "))
    except ValueError:
        print("❌ Monto inválido")
        return

    description = input("📝 Descripción: ")

    data.setdefault("expenses", [])
    data["expenses"].append({
        "category": category,
        "amount": amount,
        "description": description
    })

    save_data(data)
    print("✅ Gasto registrado correctamente")



def show_balance():
    data = load_data()
    summary = data.get("summary", {})

    diezmo = summary.get("tithe", 0)
    deudas = summary.get("debts", 0)
    ahorro = summary.get("savings", 0)
    ingresos = summary.get("income", 0)
    gastos = summary.get("expenses", 0)

    gasto_disponible = (
        ingresos
        - diezmo
        - deudas
        - ahorro
    )

    print_financial_summary(
        diezmo=diezmo,
        deudas=deudas,
        ahorro=ahorro,
        disponible=gasto_disponible
    )


def show_financial_tools_menu():
    while True:
        print("\n🧾", t("financial_tools"))
        print("1️⃣ 📊", t("monthly_report"))
        print("2️⃣ 📅", t("period_summary"))
        print("3️⃣ 📂", t("expenses_by_category"))
        print("4️⃣ 🏺", t("cash_flow"))
        print("5️⃣ 💰", t("babylon_savings"))
        print("6️⃣ 📈", t("financial_evolution"))
        print("7️⃣ 🧾", t("export_financial_evolution"))
        print("8️⃣ 📂", t("export_expenses_by_category"))
        print("9️⃣ 🏺", t("menu_export_babylon_savings"))
        print("0️⃣ ⬅️", t("back"))

        option = input("👉 " + t("select_option") + ": ").strip()

        if option == "1":
            print("📊", t("feature_coming_soon"))
        elif option == "2":
            print("📅", t("feature_coming_soon"))
        elif option == "3":
            print("📂", t("feature_coming_soon"))
        elif option == "4":
            print("🏺", t("feature_coming_soon"))
        elif option == "5":
            print("💰", t("feature_coming_soon"))
        elif option == "6":
            show_financial_evolution()
        elif option == "7":
            export_financial_evolution_txt()
        elif option == "8":
            export_expenses_by_category_txt()
        elif option == "9":
            export_babylon_savings_txt()
        elif option == "0":
            break
        else:
            print("❌", t("invalid_option"))



def show_monthly_report():
    data = load_data()

    print("\n📊", t("monthly_report"))

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    income_total = 0
    expense_total = 0

    # ---- INGRESOS ----
    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                income_total += item.get("amount", 0)
        except Exception:
            continue

    # ---- GASTOS ----
    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                expense_total += item.get("amount", 0)
        except Exception:
            expense_total += item.get("amount", 0)

    tithe = income_total * 0.10
    savings = income_total * 0.10
    available = income_total - tithe - savings - expense_total

    print("\n" + "-" * 40)
    print(f"{t('income')}: {income_total:.2f}")
    print(f"{t('expense')}: {expense_total:.2f}")
    print(f"{t('tithe')}: {tithe:.2f}")
    print(f"{t('savings')}: {savings:.2f}")
    print("-" * 40)
    print(f"{t('available')}: {available:.2f}")
    print("-" * 40)


def export_reports_menu():
    while True:
        print("\n🧾", t("export_reports"))
        print("1️⃣ ", t("export_monthly_txt"))
        print("2️⃣ ", t("export_monthly_csv"))
        print("0️⃣ ", t("back"))

        option = input("👉 " + t("select_option") + ": ").strip()

        if option == "1":
            export_monthly_report_txt()
        elif option == "2":
            export_monthly_report_csv()
        elif option == "0":
            break
        else:
            print("❌", t("invalid_option"))


def export_monthly_report_txt():
    data = load_data()

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    income_total = 0
    expense_total = 0

    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                income_total += item.get("amount", 0)
        except Exception:
            continue

    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                expense_total += item.get("amount", 0)
        except Exception:
            expense_total += item.get("amount", 0)

    tithe = income_total * 0.10
    savings = income_total * 0.10
    available = income_total - tithe - savings - expense_total

    filename = f"reporte_{year}_{month}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("🏛️ FINANZAS DE BABILONIA\n")
        f.write("Reporte mensual del oro\n\n")
        f.write(f"Periodo: {month}/{year}\n")
        f.write("-" * 35 + "\n")
        f.write(f"Ingresos : {income_total:.2f}\n")
        f.write(f"Gastos   : {expense_total:.2f}\n")
        f.write(f"Diezmo   : {tithe:.2f}\n")
        f.write(f"Ahorro   : {savings:.2f}\n")
        f.write("-" * 35 + "\n")
        f.write(f"Disponible: {available:.2f}\n")

    print(f"✅ {t('file_generated')}: {filename}")



def export_monthly_report_csv():
    import csv

    data = load_data()

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    income_total = 0
    expense_total = 0

    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                income_total += item.get("amount", 0)
        except Exception:
            continue

    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                expense_total += item.get("amount", 0)
        except Exception:
            expense_total += item.get("amount", 0)

    tithe = income_total * 0.10
    savings = income_total * 0.10
    available = income_total - tithe - savings - expense_total

    filename = f"reporte_{year}_{month}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Concepto", "Monto"])
        writer.writerow(["Ingresos", income_total])
        writer.writerow(["Gastos", expense_total])
        writer.writerow(["Diezmo", tithe])
        writer.writerow(["Ahorro", savings])
        writer.writerow(["Disponible", available])

    print(f"✅ {t('file_generated')}: {filename}")


def show_expenses_by_category():
    data = load_data()

    print("\n📂", t("expenses_by_category"))

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    categories = {}
    total_expenses = 0

    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month != month or date.year != year:
                continue
        except Exception:
            pass  # gastos antiguos sin fecha

        category = item.get("category", t("others"))
        amount = item.get("amount", 0)

        categories[category] = categories.get(category, 0) + amount
        total_expenses += amount

    if total_expenses == 0:
        print("ℹ️", t("no_data"))
        return

    # ---- MOSTRAR RESULTADO ----
    print("\n" + "-" * 40)
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        percent = (amount / total_expenses) * 100
        print(f"{cat:<20} {amount:>10.2f} ({percent:>5.1f}%)")

    print("-" * 40)
    print(f"{t('total')}: {total_expenses:.2f}")

    # ---- OPCIONES DE EXPORTACIÓN ----
    print("\n🧾", t("export_reports"))
    print("1️⃣ ", t("export_txt"))
    print("2️⃣ ", t("export_csv"))
    print("0️⃣ ", t("back"))

    option = input("👉 " + t("select_option") + ": ").strip()

    if option == "1":
        export_expenses_by_category_txt()
    elif option == "2":
        export_expenses_by_category_csv()
    elif option == "0":
        return
    else:
        print("❌", t("invalid_option"))



def export_expenses_by_category_txt():
    data = load_data()

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    categories = {}
    total_expenses = 0

    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month != month or date.year != year:
                continue
        except Exception:
            pass

        category = item.get("category", t("others"))
        amount = item.get("amount", 0)

        categories[category] = categories.get(category, 0) + amount
        total_expenses += amount

    if total_expenses == 0:
        print("ℹ️", t("no_data"))
        return

    filename = f"gastos_por_categoria_{year}_{month}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("🏛️ FINANZAS DE BABILONIA\n")
        f.write("Gastos por categoría\n\n")
        f.write(f"Periodo: {month}/{year}\n")
        f.write("-" * 35 + "\n")

        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / total_expenses) * 100
            f.write(f"{cat}: {amount:.2f} ({percent:.1f}%)\n")

        f.write("-" * 35 + "\n")
        f.write(f"Total: {total_expenses:.2f}\n")

    print(f"✅ {t('file_generated')}: {filename}")



def export_expenses_by_category_csv():
    import csv
    data = load_data()

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    categories = {}
    total_expenses = 0

    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month != month or date.year != year:
                continue
        except Exception:
            pass

        category = item.get("category", t("others"))
        amount = item.get("amount", 0)

        categories[category] = categories.get(category, 0) + amount
        total_expenses += amount

    if total_expenses == 0:
        print("ℹ️", t("no_data"))
        return

    filename = f"gastos_por_categoria_{year}_{month}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Categoría", "Monto", "Porcentaje"])

        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percent = (amount / total_expenses) * 100
            writer.writerow([cat, amount, f"{percent:.1f}%"])

    print(f"✅ {t('file_generated')}: {filename}")



def show_treasure_flow():
    data = load_data()

    print("\n🏺", t("cash_flow"))

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    income_total = 0
    expense_total = 0

    # ---- INGRESOS ----
    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                income_total += item.get("amount", 0)
        except Exception:
            continue

    # ---- GASTOS ----
    for item in data.get("expenses", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                expense_total += item.get("amount", 0)
        except Exception:
            expense_total += item.get("amount", 0)

    if income_total == 0 and expense_total == 0:
        print("ℹ️", t("no_data"))
        return

    tithe = income_total * 0.10
    savings = income_total * 0.10
    available = income_total - tithe - savings - expense_total

    # ---- VISUAL ASCII ----
    max_value = max(income_total, expense_total, tithe + savings)
    scale = 30  # ancho de barra

    def bar(value):
        if max_value == 0:
            return ""
        length = int((value / max_value) * scale)
        return "█" * length

    print("\n" + "-" * 40)
    print(f"{t('income'):<12} | {bar(income_total)} {income_total:.2f}")
    print(f"{t('expense'):<12} | {bar(expense_total)} {expense_total:.2f}")
    print(f"{t('tithe'):<12} | {bar(tithe)} {tithe:.2f}")
    print(f"{t('savings'):<12} | {bar(savings)} {savings:.2f}")
    print("-" * 40)
    print(f"{t('available')}: {available:.2f}")


def show_babylon_savings():
    data = load_data()

    print("\n💰", t("babylon_savings"))

    try:
        month = int(input("📅 Mes (1-12): "))
        year = int(input("📆 Año (YYYY): "))
    except ValueError:
        print("❌", t("invalid_option"))
        return

    total_savings = data.get("summary", {}).get("savings", 0)

    monthly_income = 0
    monthly_savings = 0

    # ---- INGRESOS DEL MES ----
    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            if date.month == month and date.year == year:
                amount = item.get("amount", 0)
                monthly_income += amount
        except Exception:
            continue

    monthly_savings = monthly_income * 0.10

    # ---- PROMEDIO HISTÓRICO ----
    months_with_income = set()
    for item in data.get("income_records", []):
        try:
            date = datetime.fromisoformat(item.get("date"))
            months_with_income.add((date.year, date.month))
        except Exception:
            continue

    avg_savings = 0
    if months_with_income:
        avg_savings = total_savings / len(months_with_income)

    # ---- RESULTADO ----
    print("\n" + "-" * 40)
    print(f"{t('total_savings')}: {total_savings:.2f}")
    print(f"{t('monthly_savings')}: {monthly_savings:.2f}")
    print(f"{t('average_savings')}: {avg_savings:.2f}")
    print("-" * 40)

    # ---- MENSAJE FILOSÓFICO ----
    if monthly_income == 0:
        print("ℹ️", t("no_data"))
    elif monthly_savings >= monthly_income * 0.10:
        print("🏛️", t("savings_success"))
    else:
        print("⚠️", t("savings_warning"))



def show_financial_evolution():
    data = load_data()

    print("\n📈", t("financial_evolution"))

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
        movements.setdefault(key, {
            "income": 0.0,
            "expense": 0.0,
            "saving": 0.0
        })

        movements[key]["income"] += float(item.get("amount", 0))

    # --- Gastos ---
    for item in data.get("expenses", []):
        date = parse_date(item)
        if not date:
            continue

        key = f"{date.year}-{date.month:02d}"
        movements.setdefault(key, {
            "income": 0.0,
            "expense": 0.0,
            "saving": 0.0
        })

        movements[key]["expense"] += float(item.get("amount", 0))

    if not movements:
        print("ℹ️", t("no_data"))
        return

    # --- Ahorro babilónico (10%) ---
    for values in movements.values():
        values["saving"] = values["income"] * 0.10

    print("\n" + "-" * 50)
    balance_accumulated = 0.0

    for period in sorted(movements.keys()):
        income = movements[period]["income"]
        expense = movements[period]["expense"]
        saving = movements[period]["saving"]

        balance = income - expense - saving
        balance_accumulated += balance

        print(f"📅 {period}")
        print(f"   💰 {t('income')}: {income:.2f}")
        print(f"   📉 {t('expense')}: {expense:.2f}")
        print(f"   🏺 {t('savings')}: {saving:.2f}")
        print(f"   📊 {t('balance')}: {balance_accumulated:.2f}")
        print("-" * 50)



def show_financial_tools_menu():
    while True:
        print("\n🧾", t("financial_tools"))
        print("1️⃣ 📈", t("menu_financial_evolution"))
        print("2️⃣ 🧾", t("menu_export_evolution"))
        print("0️⃣ ⬅️", t("back"))

        option = input("👉 " + t("select_option") + ": ")

        if option == "1":
            show_financial_evolution()
        elif option == "2":
            export_financial_evolution_txt()
        elif option == "0":
            break
        else:
            print("❌", t("invalid_option"))
