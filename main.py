

import seguridad as seguridad
import calculadora
import matplotlib.pyplot as plt
from datetime import datetime
import copy
import csv
import shutil
import os
import json
import reglas



# ⚠️ IMPORTANTE:
# Los datos reales de la aplicación se guardan en:
# C:\Users\<Usuario>\AppData\Roaming\BabiloniaFinanzas
# NO usar datos.json del proyecto ni de /dist

APP_DIR = os.path.join(os.environ["APPDATA"], "BabiloniaFinanzas")
os.makedirs(APP_DIR, exist_ok=True)

RUTA_DATOS = os.path.join(APP_DIR, "datos.json")
RUTA_LOG = os.path.join(APP_DIR, "log.txt")


# ==============================
# CONFIGURACIÓN GENERAL 
# ==============================
MODO_PRUEBAS = False  # 🔁 Cambiar a False cuando uses datos reales


CATEGORIAS_GASTOS = [
    "Alimentación",
    "Transporte",
    "Vivienda",
    "Servicios",
    "Educación",
    "Salud",
    "Ocio",
    "Otros"
]


def guardar_datos(datos):
    try:
        with open(RUTA_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

        with open(RUTA_LOG, "a", encoding="utf-8") as log:
            log.write(f"GUARDADO OK - {datetime.now()}\n")

    except Exception as e:
        with open(RUTA_LOG, "a", encoding="utf-8") as log:
            log.write(f"ERROR AL GUARDAR: {e}\n")
        raise


def cargar_datos():
    if os.path.exists(RUTA_DATOS):
        with open(RUTA_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def respaldo_datos():
    if os.path.exists("datos.json"):
        if not os.path.exists("respaldos"):
            os.mkdir("respaldos")

        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shutil.copy("datos.json", f"respaldos/datos_{fecha}.json")


def reiniciar_datos():
    if not MODO_PRUEBAS:
        print("🚫 Reinicio bloqueado (Modo Producción activado).")
        return

    confirmacion = input("⚠️ Esto borrará TODOS los datos. ¿Confirmar? (si/no):\n ").lower()
    if confirmacion != "si":
        print("❌ Operación cancelada.")
        return

    datos_iniciales = {
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


    guardar_datos(datos_iniciales)
    print("🧹 Datos reiniciados correctamente (Modo Pruebas).")


def registrar_ingreso():
    datos = cargar_datos()

    if not datos["abierto"]:
        print("🔒 El mes está cerrado. No se pueden registrar movimientos.")
        return

    # --- INGRESO ---
    try:
        monto = float(input("Ingrese el monto del ingreso:\n "))
        if monto <= 0:
            print("❌ El monto debe ser mayor a 0")
            return
    except ValueError:
        print("❌ Ingrese un número válido")
        return

    # --- VALIDACIÓN SI / NO (DEUDAS) ---
    while True:
        respuesta = input("¿Tiene deudas? (si/no):\n ").strip().lower()

        if respuesta in ["si", "sí"]:
            tiene_deudas = True
            break
        elif respuesta == "no":
            tiene_deudas = False
            break
        else:
            print("❌ Respuesta inválida. Escriba únicamente: si o no.")

    # --- VALIDACIÓN SI / NO (DIEZMO) ---
    while True:
        resp_diezmo = input("¿Desea pagar diezmo? (si/no):\n ").strip().lower()

        if resp_diezmo in ["si", "sí"]:
            paga_diezmo = True
            break
        elif resp_diezmo == "no":
            paga_diezmo = False
            break
        else:
            print("❌ Respuesta inválida. Escriba únicamente: si o no.")


    # --- DISTRIBUCIÓN BASE ---
    distribucion = calculadora.distribuir_ingreso(
    monto,
    tiene_deudas,
    paga_diezmo
    )

    mi_pago = distribucion["Mi pago"]

    # --- AHORRO AUTOMÁTICO DESDE MI PAGO ---
    ahorro_emergencia = mi_pago * 0.05
    ahorro_general = mi_pago * 0.05

    distribucion["Ahorro emergencia"] = ahorro_emergencia
    distribucion["Ahorro general"] = ahorro_general
    distribucion["Mi pago disponible"] = mi_pago - (ahorro_emergencia + ahorro_general)

    # --- GUARDAR INGRESO DETALLADO ---
    datos["ingresos"].append({
        "fecha": datetime.now().isoformat(),
        "monto": monto,
        "tiene_deudas": tiene_deudas,
        "distribucion": distribucion
    })

    # --- ACTUALIZAR RESUMEN ---
    for clave, valor in distribucion.items():
        if clave in datos["resumen"]:
            datos["resumen"][clave] += valor


    guardar_datos(datos)

    # --- SALIDA CLARA EN CONSOLA ---
    print("\n📊 DISTRIBUCIÓN DEL INGRESO")
    if paga_diezmo and distribucion["Diezmo"] > 0:
        print(f"Diezmo: ${distribucion['Diezmo']:,.0f}")


    print(f"Mi pago bruto: ${mi_pago:,.0f}")

    if tiene_deudas and "Deudas" in distribucion:
        print(f"Deudas: ${distribucion['Deudas']:,.0f}")

    print("\n🏦 Ahorro automático desde Mi pago:")
    print(f"  - Emergencia (5%): ${ahorro_emergencia:,.0f}")
    print(f"  - Ahorro general (5%): ${ahorro_general:,.0f}")

    print(f"\n💰 Mi pago disponible: ${distribucion['Mi pago disponible']:,.0f}")
    print(f"Gastos: ${distribucion['Gastos']:,.0f}")


def registrar_gasto():

    datos = cargar_datos()

    if not datos["abierto"]:
        print("🔒 El mes está cerrado. No se pueden registrar movimientos.")
        return

    print("\n📂 Categorías de gasto:")
    for i, categoria in enumerate(CATEGORIAS_GASTOS, start=1):
        print(f"{i:<2} {categoria}")


    try:
        opcion = int(input("Seleccione una categoría:\n "))
        if opcion < 1 or opcion > len(CATEGORIAS_GASTOS):
            print("❌ Opción inválida")
            return
        categoria = CATEGORIAS_GASTOS[opcion - 1]
    except ValueError:
        print("❌ Debe ingresar un número")
        return


    while True:
        try:
            monto = float(input("Ingrese el monto del gasto:\n "))
            if monto <= 0:
                print("❌ El monto debe ser mayor a 0")
                continue
            break
        except ValueError:
            print("❌ Ingrese un número válido")

    if monto > datos["resumen"]["Gastos"]:
        print("🚨 No tienes presupuesto suficiente para este gasto.")
        return

    datos["gastos"].append({
        "categoria": categoria,
        "monto": monto
    })

    datos["resumen"]["Gastos"] -= monto
    guardar_datos(datos)

    print(f"✅ Gasto registrado en '{categoria}' por ${monto:,.0f}")


def crear_meta():
    datos = cargar_datos()

    nombre = input("Nombre de la meta: ")
    monto_objetivo = float(input("Monto objetivo: "))

    meta = {
        "nombre": nombre,
        "objetivo": monto_objetivo,
        "ahorrado": 0
    }

    datos["metas"].append(meta)
    guardar_datos(datos)

    print(f"🎯 Meta '{nombre}' creada con objetivo ${monto_objetivo:,.0f}")

def aportar_meta():
    datos = cargar_datos()

    if not datos["metas"]:
        print("❌ No hay metas creadas")
        return

    print("\n🎯 Metas:")
    for i, meta in enumerate(datos["metas"], start=1):
        print(f"{i}. {meta['nombre']} (${meta['ahorrado']:,.0f} / ${meta['objetivo']:,.0f})")

    try:
        opcion = int(input("Seleccione una meta (número):\n "))
        if opcion < 1 or opcion > len(datos["metas"]):
            print("❌ Opción fuera de rango")
            return
    except ValueError:
        print("❌ Debe ingresar un número")
        return

    try:
        monto = float(input("Monto a aportar: "))
        if monto <= 0:
            print("❌ El monto debe ser mayor a 0")
            return
    except ValueError:
        print("❌ Monto inválido")
        return

    if monto > datos["ahorro"]["total"]:
        print("🚨 No tienes ahorro suficiente")
        return

    indice = opcion - 1
    datos["ahorro"]["total"] -= monto
    datos["metas"][indice]["ahorrado"] += monto

    guardar_datos(datos)
    print("✅ Aporte realizado correctamente")


def grafica_gastos():
    datos = cargar_datos()

    if not datos["gastos"]:
        print("❌ No hay gastos registrados")
        return

    categorias = {}
    for gasto in datos["gastos"]:
        cat = gasto["categoria"]
        categorias[cat] = categorias.get(cat, 0) + gasto["monto"]

    nombres = list(categorias.keys())
    valores = list(categorias.values())

    plt.figure()
    plt.bar(nombres, valores)
    plt.title("Gastos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Monto")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafica_metas():
    datos = cargar_datos()

    if not datos["metas"]:
        print("❌ No hay metas registradas")
        return

    nombres = [meta["nombre"] for meta in datos["metas"]]
    porcentajes = [
        (meta["ahorrado"] / meta["objetivo"]) * 100
        for meta in datos["metas"]
    ]

    plt.figure()
    plt.bar(nombres, porcentajes)
    plt.title("Progreso de metas (%)")
    plt.ylabel("Porcentaje completado")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def reporte_financiero():
    datos = cargar_datos()

    print("\n📊 REPORTE FINANCIERO GENERAL")

    total_ingresos = sum(i["monto"] for i in datos["ingresos"])
    total_gastos = sum(g["monto"] for g in datos["gastos"])

    print(f"Ingresos totales: ${total_ingresos:,.0f}")
    print(f"Gastos totales:   ${total_gastos:,.0f}")

    balance = total_ingresos - total_gastos
    print(f"Balance:          ${balance:,.0f}")

    print("\n🏦 AHORROS")
    print(f"Ahorro emergencia: ${datos['resumen']['Ahorro emergencia']:,.0f}")
    print(f"Ahorro general: ${datos['resumen']['Ahorro general']:,.0f}")
    print(f"Ahorro total: ${datos['resumen']['Ahorro total']:,.0f}")


def verificar_cierre_mes(datos):
    mes_actual = datetime.now().strftime("%Y-%m")

    # Inicializaciones seguras
    if "mes_actual" not in datos:
        datos["mes_actual"] = mes_actual

    if "historial" not in datos:
        datos["historial"] = []

    if "resumen" not in datos:
        datos["resumen"] = {
            "Diezmo": 0,
            "Mi pago": 0,
            "Deudas": 0,
            "Gastos": 0,
            "Ahorro emergencia": 0,
            "Ahorro general": 0,
            "Mi pago disponible": 0
        }

    mes_guardado = datos["mes_actual"]

    # Si cambió el mes → cerrar mes anterior
    if mes_guardado != mes_actual:
        datos["historial"].append({
            "mes": mes_guardado,
            "resumen": copy.deepcopy(datos["resumen"])
        })

        # Reiniciar mes
        datos["mes_actual"] = mes_actual
        datos["resumen"] = {
            "Diezmo": 0,
            "Mi pago": 0,
            "Deudas": 0,
            "Gastos": 0,
            "Ahorro emergencia": 0,
            "Ahorro general": 0,
            "Mi pago disponible": 0
        }

        datos["ingresos"] = []
        datos["gastos"] = []

        guardar_datos(datos)

        print("📦 Mes cerrado automáticamente.")



def registrar_ajuste():
    datos = cargar_datos()

    if not datos["abierto"]:
        print("🔒 No se pueden hacer ajustes en meses cerrados.")
        return

    descripcion = input("Descripción del ajuste:\n ")
    monto = float(input("Monto del ajuste (+ o -): "))

    datos["ajustes"].append({
        "fecha": datetime.now().isoformat(),
        "descripcion": descripcion,
        "monto": monto
    })

    datos["resumen"]["Gastos"] += monto
    guardar_datos(datos)

    print("✏️ Ajuste registrado (queda en historial).")

def ver_historial():
    datos = cargar_datos()

    print("\n📚 HISTORIAL FINANCIERO")
    for mes in datos["historial"]:
        print(f"\n🗓️ Mes: {mes['mes']}")
        for k, v in mes["resumen"].items():
            print(f"{k}: ${v:,.0f}")


def obtener_historial():
    datos = cargar_datos()
    return datos.get("historial", [])



def registrar_ingreso_desde_ui(monto, tiene_deudas, paga_diezmo):
    datos = cargar_datos()

    # === Inicialización segura de estructura ===
    datos.setdefault("abierto", True)
    datos.setdefault("ingresos", [])
    datos.setdefault("gastos", [])
    datos.setdefault("historial", [])
    datos.setdefault("resumen", {})

    for clave in [
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
        datos["resumen"].setdefault(clave, 0)

    # Si no está abierto, no hacer nada
    if not datos.get("abierto", True):
        return None

    ingreso = float(monto)

    # ─── Distribución base desde calculadora ───
    distribucion = calculadora.distribuir_ingreso(
        ingreso,
        tiene_deudas,
        paga_diezmo
    )

    # ─── Mi pago (10% fijo) ───
    mi_pago = distribucion["Mi pago"]

    # ─── Ahorros automáticos (salen SOLO de mi pago) ───
    ahorro_emergencia = mi_pago * 0.05
    ahorro_general = mi_pago * 0.05
    ahorro_total = ahorro_emergencia + ahorro_general

    distribucion["Ahorro emergencia"] = ahorro_emergencia
    distribucion["Ahorro general"] = ahorro_general
    distribucion["Ahorro total"] = ahorro_total
    distribucion["Mi pago disponible"] = mi_pago - ahorro_total

    # ─── ✅ CORRECCIÓN CLAVE: GASTOS CORRECTOS ───
    diezmo = distribucion.get("Diezmo", 0)
    deudas = distribucion.get("Deudas", 0)

    gastos = ingreso - diezmo - deudas - mi_pago
    distribucion["Gastos"] = gastos

    # ─── Guardar ingreso ───
    datos["ingresos"].append({
        "fecha": datetime.now().isoformat(),
        "monto": ingreso,
        "tiene_deudas": tiene_deudas,
        "distribucion": distribucion
    })

    # ─── Actualizar resumen ───
    datos["resumen"]["Ingresos"] += ingreso
    datos["resumen"]["Diezmo"] += diezmo
    datos["resumen"]["Deudas"] += deudas
    datos["resumen"]["Gastos"] += gastos
    datos["resumen"]["Mi pago"] += mi_pago
    datos["resumen"]["Ahorro emergencia"] += ahorro_emergencia
    datos["resumen"]["Ahorro general"] += ahorro_general

    datos["resumen"]["Ahorro total"] = (
        datos["resumen"]["Ahorro emergencia"] +
        datos["resumen"]["Ahorro general"]
    )

    datos["resumen"]["Mi pago disponible"] = (
        datos["resumen"]["Mi pago"] -
        datos["resumen"]["Ahorro total"]
    )

    guardar_datos(datos)
    return distribucion



def registrar_gasto_desde_ui(monto, categoria):
    datos = cargar_datos()

    if datos["resumen"]["Gastos"] < monto:
        return False

    datos["gastos"].append({
        "monto": monto,
        "categoria": categoria
    })

    datos["resumen"]["Gastos"] -= monto

    guardar_datos(datos)
    return True


def obtener_reporte_mensual():
    datos = cargar_datos()
    resumen = datos.get("resumen", {})

    reporte = {
        "Diezmo": resumen.get("Diezmo", 0),
        "Deudas": resumen.get("Deudas", 0),
        "Gastos": resumen.get("Gastos", 0),
        "Mi pago": resumen.get("Mi pago", 0),
        "Ahorro emergencia": resumen.get("Ahorro emergencia", 0),
        "Ahorro general": resumen.get("Ahorro general", 0),
        "Ahorro total": resumen.get("Ahorro total", 0),
        "Mi pago disponible": resumen.get("Mi pago disponible", 0),
    }

    return reporte

def obtener_historial():
    datos = cargar_datos()
    return datos.get("historial", [])



def grafica_comparacion_mensual():
    historial = obtener_historial()

    if len(historial) < 1:
        print("❌ No hay meses suficientes para comparar.")
        return False

    meses = []
    ingresos = []
    gastos = []
    ahorros = []

    for mes in historial:
        resumen = mes["resumen"]

        meses.append(mes["mes"])
        ingresos.append(
            resumen.get("Mi pago", 0) +
            resumen.get("Diezmo", 0) +
            resumen.get("Deudas", 0)
        )
        gastos.append(resumen.get("Gastos", 0))
        ahorros.append(
            resumen.get("Ahorro emergencia", 0) +
            resumen.get("Ahorro general", 0)
        )

    plt.figure()
    plt.plot(meses, ingresos, label="Ingresos")
    plt.plot(meses, gastos, label="Gastos")
    plt.plot(meses, ahorros, label="Ahorro")

    plt.title("Comparación mensual")
    plt.xlabel("Mes")
    plt.ylabel("Monto")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return True


def comparar_meses(mes1, mes2):
    historial = obtener_historial()

    m1 = next((m for m in historial if m["mes"] == mes1), None)
    m2 = next((m for m in historial if m["mes"] == mes2), None)

    if not m1 or not m2:
        return None

    comparacion = {}

    for clave in m1["resumen"]:
        comparacion[clave] = m2["resumen"].get(clave, 0) - m1["resumen"].get(clave, 0)

    return comparacion


def obtener_estado_mes():
    datos = cargar_datos()
    return datos.get("abierto", True)

def exportar_historial_csv(ruta="historial_financiero.csv"):
    datos = cargar_datos()
    historial = datos.get("historial", [])

    if not historial:
        return False

    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mes", "Concepto", "Monto"])

        for mes in historial:
            for k, v in mes["resumen"].items():
                writer.writerow([mes["mes"], k, v])

    return True


def analisis_financiero():
    datos = cargar_datos()
    historial = datos.get("historial", [])

    if len(historial) < 2:
        return "No hay suficientes datos para análisis."

    actual = historial[-1]["resumen"]
    anterior = historial[-2]["resumen"]

    mensajes = []

    if actual.get("Gastos", 0) > anterior.get("Gastos", 0):
        mensajes.append("⚠️ Gastaste más que el mes anterior.")

    if actual.get("Ahorro total", 0) < anterior.get("Ahorro total", 0):
        mensajes.append("⚠️ Tu ahorro disminuyó.")

    if not mensajes:
        mensajes.append("✅ Buen trabajo, tus finanzas van mejorando.")

    return "\n".join(mensajes)



def menu():
    datos = cargar_datos()
    verificar_cierre_mes(datos)

    while True:

        modo = "🧪 PRUEBAS" if MODO_PRUEBAS else "🔒 PRODUCCIÓN"
        print(f"\n🏛️ FINANZAS DE BABILONIA — {modo}")


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

        opcion = input("Seleccione una opción:\n ")

        if opcion == "1":
            registrar_ingreso()

        elif opcion == "2":
            registrar_gasto()

        elif opcion == "3":
            crear_meta()

        elif opcion == "4":
            aportar_meta()

        elif opcion == "5":
            reporte_financiero()

        elif opcion == "6":
            grafica_gastos()

        elif opcion == "7":
            grafica_metas()

        elif opcion == "8":
            reiniciar_datos()

        elif opcion == "9":
            print("👋 Hasta pronto. Protege tu oro.")
            break

        else:
            print("❌ Opción inválida")

def obtener_historial_para_grafica():
    datos = cargar_datos()
    return datos.get("historial", [])

def analizar_alertas():
    datos = cargar_datos()
    alertas = []

    resumen = datos.get("resumen", {})
    ingreso = resumen.get("Mi pago", 0)
    gastos = resumen.get("Gastos", 0)
    ahorro_total = resumen.get("Ahorro total", 0)

    if ingreso > 0:
        if gastos > ingreso * reglas.REGLAS["max_gastos_pct"]:
            alertas.append("⚠️ Gastos superan el 60% del ingreso")

        if ahorro_total < ingreso * reglas.REGLAS["min_ahorro_pct"]:
            alertas.append("⚠️ Ahorro menor al 10% del ingreso")

    # Comparación ocio
    historial = datos.get("historial", [])
    if len(historial) >= 1:
        mes_ant = historial[-1]["resumen"]
        ocio_ant = mes_ant.get("Ocio", 0)
        ocio_act = 0  # si luego separas por categoría
        if ocio_ant > 0 and ocio_act > ocio_ant * (1 + reglas.REGLAS["alerta_ocio_pct"]):
            alertas.append("⚠️ Ocio aumentó más del 20%")

    return alertas

            
if __name__ == "__main__":
    menu()
