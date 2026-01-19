
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
    "Alimentación",
    "Transporte",
    "Vivienda",
    "Servicios",
    "Educación",
    "Salud",
    "Ocio",
    "Otros"
]


def save_data(data):
    # Guardar datos en JSON y log
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"GUARDADO OK - {datetime.now()}\n")

    except Exception as e:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(f"ERROR AL GUARDAR: {e}\n")
        raise


def load_data():
    # Cargar datos desde JSON
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


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
        print("🚫 Reinicio bloqueado (Modo Producción activado).")
        return

    confirmation = input("⚠️ Esto borrará TODOS los datos. ¿Confirmar? (si/no):\n ").lower()
    if confirmation != "si":
        print("❌ Operación cancelada.")
        return

    initial_data = {
        "mes_actual": datetime.now().strftime("%Y-%m"),
        "abierto": True,
        "ingresos": [],
        "gastos": [],
        "metas": [],
        "cierres": [],
        "historial": [],
        "ajustes": [],
        "ahorro": {
            "emergencia": 0,
            "total": 0
        },
        "resumen": {
            "Diezmo": 0,
            "Mi pago": 0,
            "Mi pago disponible": 0,
            "Deudas": 0,
            "Gastos": 0,
            "Ahorro emergencia": 0,
            "Ahorro general": 0
        }
    }

    save_data(initial_data)
    print("🧹 Datos reiniciados correctamente (Modo Pruebas).")


def register_income():
    # Registrar un ingreso nuevo
    data = load_data()

    if not data["abierto"]:
        print("🔒 El mes está cerrado. No se pueden registrar movimientos.")
        return

    # --- INGRESO ---
    try:
        amount = float(input("Ingrese el monto del ingreso:\n "))
        if amount <= 0:
            print("❌ El monto debe ser mayor a 0")
            return
    except ValueError:
        print("❌ Ingrese un número válido")
        return

    # --- VALIDACIÓN SI / NO (DEUDAS) ---
    while True:
        response = input("¿Tiene deudas? (si/no):\n ").strip().lower()

        if response in ["si", "sí"]:
            has_debts = True
            break
        elif response == "no":
            has_debts = False
            break
        else:
            print("❌ Respuesta inválida. Escriba únicamente: si o no.")

    # --- VALIDACIÓN SI / NO (DIEZMO) ---
    while True:
        tithe_resp = input("¿Desea pagar diezmo? (si/no):\n ").strip().lower()

        if tithe_resp in ["si", "sí"]:
            pay_tithe = True
            break
        elif tithe_resp == "no":
            pay_tithe = False
            break
        else:
            print("❌ Respuesta inválida. Escriba únicamente: si o no.")


    # --- DISTRIBUCIÓN BASE ---
    distribution = calculator.distribuir_ingreso(
        amount,
        has_debts,
        pay_tithe
    )

    my_payment = distribution["Mi pago"]

    # --- AHORRO AUTOMÁTICO DESDE MI PAGO ---
    emergency_saving = my_payment * 0.05
    general_saving = my_payment * 0.05

    distribution["Ahorro emergencia"] = emergency_saving
    distribution["Ahorro general"] = general_saving
    distribution["Mi pago disponible"] = my_payment - (emergency_saving + general_saving)

    # --- GUARDAR INGRESO DETALLADO ---
    data["ingresos"].append({
        "fecha": datetime.now().isoformat(),
        "monto": amount,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # --- ACTUALIZAR RESUMEN ---
    for key, value in distribution.items():
        if key in data["resumen"]:
            data["resumen"][key] += value

    save_data(data)

    # --- SALIDA CLARA EN CONSOLA ---
    print("\n📊 DISTRIBUCIÓN DEL INGRESO")
    if pay_tithe and distribution["Diezmo"] > 0:
        print(f"Diezmo: ${distribution['Diezmo']:,.0f}")

    print(f"Mi pago bruto: ${my_payment:,.0f}")

    if has_debts and "Deudas" in distribution:
        print(f"Deudas: ${distribution['Deudas']:,.0f}")

    print("\n🏦 Ahorro automático desde Mi pago:")
    print(f"  - Emergencia (5%): ${emergency_saving:,.0f}")
    print(f"  - Ahorro general (5%): ${general_saving:,.0f}")

    print(f"\n💰 Mi pago disponible: ${distribution['Mi pago disponible']:,.0f}")
    print(f"Gastos: ${distribution['Gastos']:,.0f}")







#SE TRADUCE HASTA AQUI 1


def register_expense():

    data = load_data()

    if not data["abierto"]:
        print("🔒 El mes está cerrado. No se pueden registrar movimientos.")
        return

    print("\n📂 Categorías de gasto:")
    for i, category in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"{i:<2} {category}")


    try:
        option = int(input("Seleccione una categoría:\n "))
        if option < 1 or option > len(EXPENSE_CATEGORIES):
            print("❌ Opción inválida")
            return
        category = EXPENSE_CATEGORIES[option - 1]
    except ValueError:
        print("❌ Debe ingresar un número")
        return


    while True:
        try:
            amount = float(input("Ingrese el monto del gasto:\n "))
            if amount <= 0:
                print("❌ El monto debe ser mayor a 0")
                continue
            break
        except ValueError:
            print("❌ Ingrese un número válido")

    if amount > data["resumen"]["Gastos"]:
        print("🚨 No tienes presupuesto suficiente para este gasto.")
        return

    data["gastos"].append({
        "categoria": category,
        "monto": amount
    })

    data["resumen"]["Gastos"] -= amount
    save_data(data)

    print(f"✅ Gasto registrado en '{category}' por ${amount:,.0f}")


def create_goal():
    data = load_data()

    name = input("Nombre de la meta: ")
    target_amount = float(input("Monto objetivo: "))

    goal = {
        "nombre": name,
        "objetivo": target_amount,
        "ahorrado": 0
    }

    data["metas"].append(goal)
    save_data(data)

    print(f"🎯 Meta '{name}' creada con objetivo ${target_amount:,.0f}")


def contribute_goal():
    data = load_data()

    if not data["metas"]:
        print("❌ No hay metas creadas")
        return

    print("\n🎯 Metas:")
    for i, goal in enumerate(data["metas"], start=1):
        print(f"{i}. {goal['nombre']} (${goal['ahorrado']:,.0f} / ${goal['objetivo']:,.0f})")

    try:
        option = int(input("Seleccione una meta (número):\n "))
        if option < 1 or option > len(data["metas"]):
            print("❌ Opción fuera de rango")
            return
    except ValueError:
        print("❌ Debe ingresar un número")
        return

    try:
        amount = float(input("Monto a aportar: "))
        if amount <= 0:
            print("❌ El monto debe ser mayor a 0")
            return
    except ValueError:
        print("❌ Monto inválido")
        return

    if amount > data["ahorro"]["total"]:
        print("🚨 No tienes ahorro suficiente")
        return

    index = option - 1
    data["ahorro"]["total"] -= amount
    data["metas"][index]["ahorrado"] += amount

    save_data(data)
    print("✅ Aporte realizado correctamente")


def expense_chart():
    data = load_data()

    if not data["gastos"]:
        print("❌ No hay gastos registrados")
        return

    categories = {}
    for expense in data["gastos"]:
        cat = expense["categoria"]
        categories[cat] = categories.get(cat, 0) + expense["monto"]

    names = list(categories.keys())
    values = list(categories.values())

    plt.figure()
    plt.bar(names, values)
    plt.title("Gastos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Monto")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def goals_chart():
    data = load_data()

    if not data["metas"]:
        print("❌ No hay metas registradas")
        return

    names = [goal["nombre"] for goal in data["metas"]]
    percentages = [
        (goal["ahorrado"] / goal["objetivo"]) * 100
        for goal in data["metas"]
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

    print("\n📊 REPORTE FINANCIERO GENERAL")

    total_income = sum(i["monto"] for i in data["ingresos"])
    total_expenses = sum(e["monto"] for e in data["gastos"])

    print(f"Ingresos totales: ${total_income:,.0f}")
    print(f"Gastos totales:   ${total_expenses:,.0f}")

    balance = total_income - total_expenses
    print(f"Balance:          ${balance:,.0f}")

    print("\n🏦 AHORROS")
    print(f"Ahorro emergencia: ${data['resumen']['Ahorro emergencia']:,.0f}")
    print(f"Ahorro general: ${data['resumen']['Ahorro general']:,.0f}")
    print(f"Ahorro total: ${data['resumen']['Ahorro total']:,.0f}")


def check_month_close(data):
    current_month = datetime.now().strftime("%Y-%m")

    # Inicializaciones seguras
    if "mes_actual" not in data:
        data["mes_actual"] = current_month

    if "historial" not in data:
        data["historial"] = []

    if "resumen" not in data:
        data["resumen"] = {
            "Diezmo": 0,
            "Mi pago": 0,
            "Deudas": 0,
            "Gastos": 0,
            "Ahorro emergencia": 0,
            "Ahorro general": 0,
            "Mi pago disponible": 0
        }

    saved_month = data["mes_actual"]

    # Si cambió el mes → cerrar mes anterior
    if saved_month != current_month:
        data["historial"].append({
            "mes": saved_month,
            "resumen": copy.deepcopy(data["resumen"])
        })

        # Reiniciar mes
        data["mes_actual"] = current_month
        data["resumen"] = {
            "Diezmo": 0,
            "Mi pago": 0,
            "Deudas": 0,
            "Gastos": 0,
            "Ahorro emergencia": 0,
            "Ahorro general": 0,
            "Mi pago disponible": 0
        }

        data["ingresos"] = []
        data["gastos"] = []

        save_data(data)

        print("📦 Mes cerrado automáticamente.")


def register_adjustment():
    data = load_data()

    if not data["abierto"]:
        print("🔒 No se pueden hacer ajustes en meses cerrados.")
        return

    description = input("Descripción del ajuste:\n ")
    amount = float(input("Monto del ajuste (+ o -): "))

    data["ajustes"].append({
        "fecha": datetime.now().isoformat(),
        "descripcion": description,
        "monto": amount
    })

    data["resumen"]["Gastos"] += amount
    save_data(data)

    print("✏️ Ajuste registrado (queda en historial).")


def view_history():
    data = load_data()

    print("\n📚 HISTORIAL FINANCIERO")
    for month in data["historial"]:
        print(f"\n🗓️ Mes: {month['mes']}")
        for key, value in month["resumen"].items():
            print(f"{key}: ${value:,.0f}")


def get_history():
    data = load_data()
    return data.get("historial", [])


def register_income_from_ui(amount, has_debts, pay_tithe):
    data = load_data()

    # === Inicialización segura de estructura ===
    data.setdefault("abierto", True)
    data.setdefault("ingresos", [])
    data.setdefault("gastos", [])
    data.setdefault("historial", [])
    data.setdefault("resumen", {})

    for key in [
        "Ingresos",
        "Gastos",
        "Ahorro total",
        "Diezmo",
        "Deudas",
        "Mi pago",
        "Ahorro emergencia",
        "Ahorro general",
        "Mi pago disponible"
    ]:
        data["resumen"].setdefault(key, 0)

    # Si no está abierto, no hacer nada
    if not data.get("abierto", True):
        return None

    income = float(amount)

    # ─── Distribución base desde calculadora ───
    distribution = calculator.distribuir_ingreso(
        income,
        has_debts,
        pay_tithe
    )

    # ─── Mi pago (10% fijo) ───
    my_payment = distribution["Mi pago"]

    # ─── Ahorros automáticos (salen SOLO de mi pago) ───
    emergency_saving = my_payment * 0.05
    general_saving = my_payment * 0.05
    total_saving = emergency_saving + general_saving

    distribution["Ahorro emergencia"] = emergency_saving
    distribution["Ahorro general"] = general_saving
    distribution["Ahorro total"] = total_saving
    distribution["Mi pago disponible"] = my_payment - total_saving

    # ─── ✅ CORRECCIÓN CLAVE: GASTOS CORRECTOS ───
    tithe = distribution.get("Diezmo", 0)
    debts = distribution.get("Deudas", 0)

    expenses = income - tithe - debts - my_payment
    distribution["Gastos"] = expenses

    # ─── Guardar ingreso ───
    data["ingresos"].append({
        "fecha": datetime.now().isoformat(),
        "monto": income,
        "tiene_deudas": has_debts,
        "distribucion": distribution
    })

    # ─── Actualizar resumen ───
    data["resumen"]["Ingresos"] += income
    data["resumen"]["Diezmo"] += tithe
    data["resumen"]["Deudas"] += debts
    data["resumen"]["Gastos"] += expenses
    data["resumen"]["Mi pago"] += my_payment
    data["resumen"]["Ahorro emergencia"] += emergency_saving
    data["resumen"]["Ahorro general"] += general_saving

    data["resumen"]["Ahorro total"] = (
        data["resumen"]["Ahorro emergencia"] +
        data["resumen"]["Ahorro general"]
    )

    data["resumen"]["Mi pago disponible"] = (
        data["resumen"]["Mi pago"] -
        data["resumen"]["Ahorro total"]
    )

    save_data(data)
    return distribution


def register_expense_from_ui(amount, category):
    data = load_data()

    if data["resumen"]["Gastos"] < amount:
        return False

    data["gastos"].append({
        "monto": amount,
        "categoria": category
    })

    data["resumen"]["Gastos"] -= amount

    save_data(data)
    return True





#SE TRADUCE HASTA AQUI 2

def get_monthly_report():
    data = load_data()
    summary = data.get("resumen", {})

    report = {
        "Diezmo": summary.get("Diezmo", 0),
        "Deudas": summary.get("Deudas", 0),
        "Gastos": summary.get("Gastos", 0),
        "Mi pago": summary.get("Mi pago", 0),
        "Ahorro emergencia": summary.get("Ahorro emergencia", 0),
        "Ahorro general": summary.get("Ahorro general", 0),
        "Ahorro total": summary.get("Ahorro total", 0),
        "Mi pago disponible": summary.get("Mi pago disponible", 0),
    }

    return report


def get_history():
    data = load_data()
    return data.get("historial", [])


def monthly_comparison_chart():
    history = get_history()

    if len(history) < 1:
        print("❌ No hay meses suficientes para comparar.")
        return False

    months = []
    incomes = []
    expenses = []
    savings = []

    for month in history:
        summary = month["resumen"]

        months.append(month["mes"])
        incomes.append(
            summary.get("Mi pago", 0) +
            summary.get("Diezmo", 0) +
            summary.get("Deudas", 0)
        )
        expenses.append(summary.get("Gastos", 0))
        savings.append(
            summary.get("Ahorro emergencia", 0) +
            summary.get("Ahorro general", 0)
        )

    plt.figure()
    plt.plot(months, incomes, label="Ingresos")
    plt.plot(months, expenses, label="Gastos")
    plt.plot(months, savings, label="Ahorro")

    plt.title("Comparación mensual")
    plt.xlabel("Mes")
    plt.ylabel("Monto")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return True


def compare_months(month1, month2):
    history = get_history()

    m1 = next((m for m in history if m["mes"] == month1), None)
    m2 = next((m for m in history if m["mes"] == month2), None)

    if not m1 or not m2:
        return None

    comparison = {}

    for key in m1["resumen"]:
        comparison[key] = m2["resumen"].get(key, 0) - m1["resumen"].get(key, 0)

    return comparison


def get_month_status():
    data = load_data()
    return data.get("abierto", True)


def export_history_csv(path="financial_history.csv"):
    data = load_data()
    history = data.get("historial", [])

    if not history:
        return False

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mes", "Concepto", "Monto"])

        for month in history:
            for key, value in month["resumen"].items():
                writer.writerow([month["mes"], key, value])

    return True


def financial_analysis():
    data = load_data()
    history = data.get("historial", [])

    if len(history) < 2:
        return "No hay suficientes datos para análisis."

    current = history[-1]["resumen"]
    previous = history[-2]["resumen"]

    messages = []

    if current.get("Gastos", 0) > previous.get("Gastos", 0):
        messages.append("⚠️ Gastaste más que el mes anterior.")

    if current.get("Ahorro total", 0) < previous.get("Ahorro total", 0):
        messages.append("⚠️ Tu ahorro disminuyó.")

    if not messages:
        messages.append("✅ Buen trabajo, tus finanzas van mejorando.")

    return "\n".join(messages)


def main_menu():
    data = load_data()
    check_month_close(data)

    while True:

        mode = "🧪 PRUEBAS" if TEST_MODE else "🔒 PRODUCCIÓN"
        print(f"\n🏛️ FINANZAS DE BABILONIA — {mode}")

        print("\n🏛️ FINANZAS DE BABILONIA")
        print("1. Registrar ingreso")
        print("2. Registrar gasto")
        print("3. Crear meta financiera")
        print("4. Aportar a meta")
        print("5. Ver reporte financiero")
        print("6. Gráfica de gastos")
        print("7. Gráfica de metas")
        print("8. Reiniciar datos")
        print("9. Salir")

        option = input("Seleccione una opción:\n ")

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
            print("👋 Hasta pronto. Protege tu oro.")
            break

        else:
            print("❌ Opción inválida")


def get_history_for_chart():
    data = load_data()
    return data.get("historial", [])


def analyze_alerts():
    data = load_data()
    alerts = []

    summary = data.get("resumen", {})
    income = summary.get("Mi pago", 0)
    expenses = summary.get("Gastos", 0)
    total_saving = summary.get("Ahorro total", 0)

    if income > 0:
        if expenses > income * rules.RULES["max_expense_pct"]:
            alerts.append("⚠️ Gastos superan el 60% del ingreso")

        if total_saving < income * rules.RULES["min_saving_pct"]:
            alerts.append("⚠️ Ahorro menor al 10% del ingreso")

    # Comparación ocio
    history = data.get("historial", [])
    if len(history) >= 1:
        prev_month = history[-1]["resumen"]
        prev_leisure = prev_month.get("Ocio", 0)
        current_leisure = 0  # si luego separas por categoría
        if prev_leisure > 0 and current_leisure > prev_leisure * (1 + rules.RULES["alerta_ocio_pct"]):
            alerts.append("⚠️ Ocio aumentó más del 20%")

    return alerts


if __name__ == "__main__":
    main_menu()
