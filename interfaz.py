
import tkinter as tk
from tkinter import messagebox
import main
from tkinter import ttk
import matplotlib.pyplot as plt
from reglas import CATEGORIAS_GASTOS
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)



def generar_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def tiene_password():
    datos = main.cargar_datos()
    return "password_hash" in datos

def crear_password():
    ventana = tk.Tk()
    ventana.title("Crear contraseña - Babilonia Finanzas")
    ventana.geometry("300x150")

    tk.Label(ventana, text="Crea tu contraseña").pack(pady=5)
    entrada = tk.Entry(ventana, show="*")
    entrada.pack(pady=5)

    def guardar():
        password = entrada.get()
        if password == "":
            messagebox.showerror("Error", "La contraseña no puede estar vacía")
            return

        datos = main.cargar_datos()  # ← NO crear dict nuevo
        datos["password_hash"] = generar_hash(password)
        main.guardar_datos(datos)


        messagebox.showinfo("Éxito", "Contraseña creada correctamente")
        ventana.destroy()
        iniciar_app()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    ventana.mainloop()


def login():
    ventana = tk.Tk()
    ventana.title("Acceso - Babilonia Finanzas")
    ventana.geometry("300x150")

    tk.Label(ventana, text="Ingresa tu contraseña").pack(pady=5)
    entrada = tk.Entry(ventana, show="*")
    entrada.pack(pady=5)

    def validar():
        password = entrada.get()
        datos = main.cargar_datos()

        if generar_hash(password) == datos["password_hash"]:
            ventana.destroy()
            iniciar_app()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    tk.Button(ventana, text="Entrar", command=validar).pack(pady=10)
    ventana.mainloop()




COLOR_FONDO = "#f4f6f7"
COLOR_PRIMARIO = "#2c3e50"
COLOR_BOTON = "#34495e"
COLOR_BOTON_SEC = "#5dade2"
COLOR_SALIR = "#c0392b"
COLOR_TEXTO = "white"



# ==============================
# CONFIGURACIÓN DE LA VENTANA
# ==============================


def iniciar_app():  
    global ventana
    ventana = tk.Tk()
    ventana.title("🏛️ Finanzas de Babilonia")
    ventana.geometry("400x500")
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)


    # --- TÍTULO ---
    titulo = tk.Label(
        ventana,
        text="FINANZAS DE BABILONIA",
        font=("Arial", 16, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRIMARIO
    )
    titulo.pack(pady=20)


    # --- TEXTO INFORMATIVO ---
    descripcion = tk.Label(
        ventana,
        text="Aplicación de finanzas personales\nbasada en principios de Babilonia",
        font=("Arial", 10),
        justify="center",
        bg=COLOR_FONDO,
        fg=COLOR_PRIMARIO
    )
    descripcion.pack(pady=10)




        # --- FRAME PRINCIPAL (botones visibles) ---
    frame_principal = tk.Frame(ventana)
    frame_principal.pack(pady=10)



    # --- BOTONES (CON FUNCIÓN) ---

    boton_estilizado(
        frame_principal,
        "Registrar ingreso",
        ventana_ingreso
    ).pack(pady=8)

    boton_estilizado(
        frame_principal, 
        "Registrar gasto", 
        ventana_gasto
    ).pack(pady=8)

    boton_estilizado(
        frame_principal, 
        "Ver reporte", 
        ventana_reporte
    ).pack(pady=8)

    boton_estilizado(
        frame_principal,
        "📊 Herramientas financieras",
        ventana_herramientas,
        COLOR_BOTON_SEC
    ).pack(pady=10)

    boton_estilizado(
        ventana,
        "Salir",
        ventana.quit,
        COLOR_SALIR
    ).pack(pady=30)



    ventana.mainloop()


def boton_estilizado(parent, texto, comando, color=COLOR_BOTON):
    return tk.Button(
        parent,
        text=texto,
        width=25,
        bg=color,
        fg=COLOR_TEXTO,
        activebackground="#1f618d",
        relief="flat",
        command=comando
    )


def ventana_herramientas():

    global herramientas

    herramientas = tk.Toplevel()
    herramientas.configure(bg=COLOR_FONDO)
    herramientas.transient(ventana)      # pertenece a la ventana principal
    herramientas.grab_set()       # bloquea la ventana principal
    herramientas.title("📊 Herramientas financieras")
    herramientas.geometry("380x450")
    herramientas.resizable(False, False)

    tk.Label(
        herramientas,
        text="Herramientas financieras",
        font=("Arial", 14, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRIMARIO
    ).pack(pady=15)


    tk.Button(
        herramientas,
        text="Ver historial mensual",
        width=30,
        command=ventana_historial
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="Comparar meses",
        width=30,
        command=ventana_comparacion
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="Ver alertas",
        width=30,
        command=ventana_alertas
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="📈 Ver gráfica mensual",
        width=30,
        command=ventana_grafica_mensual
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="💾 Exportar historial CSV",
        width=30,
        command=exportar_csv
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="🧠 Análisis financiero",
        width=30,
        command=ventana_analisis
    ).pack(pady=8)

    tk.Button(
        herramientas,
        text="Cerrar",
        width=30,
        command=herramientas.destroy
    ).pack(pady=20)




def ventana_ingreso():
    win = tk.Toplevel()
    win.title("Registrar ingreso")

    tk.Label(win, text="Monto del ingreso").pack(pady=5)
    entry_monto = tk.Entry(win)
    entry_monto.pack(pady=5)

    tk.Label(win, text="¿Tiene deudas?").pack(pady=5)
    var_deudas = tk.StringVar(value="no")

    tk.Radiobutton(win, text="Sí", variable=var_deudas, value="si").pack()
    tk.Radiobutton(win, text="No", variable=var_deudas, value="no").pack()


    tk.Label(win, text="¿Desea pagar diezmo?").pack(pady=5)
    var_diezmo = tk.StringVar(value="no")

    tk.Radiobutton(win, text="Sí", variable=var_diezmo, value="si").pack()
    tk.Radiobutton(win, text="No", variable=var_diezmo, value="no").pack()


    resultado_frame = tk.Frame(win)
    resultado_frame.pack(pady=10)


    def guardar():

        for widget in resultado_frame.winfo_children():
            widget.destroy()


        try:
            if not entry_monto.get().strip():
                messagebox.showerror("Error", "Debe ingresar un monto")
                return

            monto_texto = entry_monto.get().strip()

            try:
                monto = float(monto_texto)
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números, sin puntos ni comas.")
                return


            tiene_deudas = var_deudas.get() == "si"
            paga_diezmo = var_diezmo.get() == "si"


            distribucion = main.registrar_ingreso_desde_ui(
                monto,
                tiene_deudas,
                paga_diezmo
            )

            if distribucion is None:
                messagebox.showwarning(
                    "Ingreso no guardado",
                    "⚠️ El período financiero está cerrado.\nNo se pueden registrar ingresos."
                )
                return


            
            tk.Label(resultado_frame, text="📊 Distribución del ingreso", font=("Arial", 12, "bold")).pack()

            for k, v in distribucion.items():
                tk.Label(resultado_frame, text=f"{k}: ${v:,.0f}").pack()
    
            # ✅ MENSAJE DE CONFIRMACIÓN
            messagebox.showinfo(
                "Ingreso guardado",
                "✅ El ingreso fue registrado correctamente"
            )

            # ✅ CERRAR VENTANA
            win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error real detectado",
                f"Ocurrió este error:\n\n{e}"
            )


    tk.Button(
        win,
        text="Guardar ingreso",
        command=guardar
    ).pack(pady=10)


def ventana_gasto():
    win = tk.Toplevel()
    win.title("Registrar gasto")

    tk.Label(win, text="Monto del gasto").pack()
    entry_monto = tk.Entry(win)
    entry_monto.pack(pady=5)


    categoria_var = tk.StringVar(value=CATEGORIAS_GASTOS[0])

    tk.Label(win, text="Categoría").pack()
    tk.OptionMenu(win, categoria_var, *CATEGORIAS_GASTOS).pack(pady=5)

    entry_otro = tk.Entry(win)
    entry_otro.pack(pady=5)
    entry_otro.pack_forget()

    def on_categoria_change(*args):
        if categoria_var.get() == "Otros":
            entry_otro.pack()
        else:
            entry_otro.pack_forget()

    categoria_var.trace_add("write", on_categoria_change)

    def guardar_gasto():
        try:
            if not entry_monto.get().strip():
                messagebox.showerror("Error", "Debe ingresar un monto")
                return

            monto = float(entry_monto.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return


            categoria = categoria_var.get()

            if categoria == "Otros":
                categoria = entry_otro.get().strip()
                if not categoria:
                    messagebox.showerror("Error", "Ingrese el nombre del gasto")
                    return

            exito = main.registrar_gasto_desde_ui(monto, categoria)

            if not exito:
                messagebox.showerror(
                    "Fondos insuficientes",
                    "No hay saldo disponible en Gastos"
                )
                return

            messagebox.showinfo("Éxito", "Gasto registrado correctamente")
            win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error inesperado",
                f"Ocurrió un error:\n{e}"
            )



    # ✅ UN SOLO BOTÓN
    tk.Button(
        win,
        text="Guardar gasto",
        command=guardar_gasto
    ).pack(pady=10)


def ventana_reporte():
    win = tk.Toplevel()
    win.title("📊 Reporte mensual")

    reporte = main.obtener_reporte_mensual()
    estado_mes = "Abierto" if main.obtener_estado_mes() else "Cerrado"

    if not reporte:
        tk.Label(
            win,
            text="No hay datos disponibles para mostrar.",
            fg="red"
        ).pack(pady=10)
        return

    tk.Label(
        win,
        text=f"Mes abierto o cerrado: {estado_mes}",
        font=("Arial", 10, "italic")
    ).pack(pady=5)


    # ─── Orden correcto del reporte ───
    orden_reporte = [
        "Diezmo",
        "Mi pago",
        "Mi pago disponible",
        "Ahorro emergencia",
        "Ahorro general",
        "Ahorro total",
        "Deudas",
        "Gastos"
    ]

    for clave in orden_reporte:
        valor = reporte.get(clave, 0)
        tk.Label(
            win,
            text=f"{clave}: ${valor:,.0f}",
            anchor="w"
        ).pack(fill="x")


    tk.Button(
        win,
        text="Cerrar",
        command=win.destroy
    ).pack(pady=10)


def ventana_historial():    
    win = tk.Toplevel()
    win.title("📚 Historial mensual")
    win.transient()
    win.grab_set()
    win.focus_force()

    historial = main.obtener_historial()

    def cerrar_ventana():
        win.grab_release()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", cerrar_ventana)


    if not historial:
        tk.Label(
            win,
            text="📭 No hay meses cerrados aún",
            font=("Arial", 11, "italic")
        ).pack(pady=10)


        win.after(0, lambda: win.grab_release())
        return


    for mes in historial:
        tk.Label(
            win,
            text=f"🗓️ {mes['mes']}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        for k, v in mes["resumen"].items():
            tk.Label(win, text=f"  {k}: ${v:,.0f}").pack(anchor="w")


def ventana_comparacion():
    try:
        ok = main.grafica_comparacion_mensual()

        if not ok:
            messagebox.showinfo(
                "Sin datos",
                "No hay meses suficientes para comparar."
            )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Ocurrió un problema:\n{e}"
        )


def ventana_grafica_mensual():
    historial = main.obtener_historial_para_grafica()

    if len(historial) < 2:
        messagebox.showinfo(
            "Gráfica",
            "Se necesitan al menos 2 meses cerrados para mostrar la gráfica"
        )
        return

    meses = [m["mes"] for m in historial]
    gastos = [m["resumen"].get("Gastos", 0) for m in historial]
    ahorros = [m["resumen"].get("Ahorro total", 0) for m in historial]




    plt.figure()
    plt.plot(meses, gastos, label="Gastos")
    plt.plot(meses, ahorros, label="Ahorro total")
    plt.title("Evolución financiera mensual")
    plt.xlabel("Mes")
    plt.ylabel("Monto ($)")
    plt.legend()

    plt.gcf().canvas.manager.window.attributes('-topmost', 1)
    plt.gcf().canvas.manager.window.attributes('-topmost', 0)

    plt.show()


def exportar_csv():
    if main.exportar_historial_csv():
        messagebox.showinfo(
            "CSV",
            "Historial exportado correctamente",
            parent=herramientas
        )
    else:
        messagebox.showwarning(
            "CSV",
            "No hay historial para exportar",
            parent=herramientas
        )



def ventana_analisis():
    mensaje = main.analisis_financiero()

    messagebox.showinfo(
        "🧠 Análisis financiero",
        mensaje,
        parent=herramientas
    )



def ventana_alertas():
    win = tk.Toplevel()
    win.title("🔔 Alertas financieras")
    win.transient()
    win.grab_set()
    win.focus_force()


    def cerrar_ventana():
        win.grab_release()
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", cerrar_ventana)


    alertas = main.analizar_alertas()

    if not alertas:
        tk.Label(win, text="✅ No hay alertas. Buen trabajo 👏").pack(pady=10)
        win.after(0, lambda: win.grab_release())
        return


    for a in alertas:
        tk.Label(win, text=a, fg="red").pack(anchor="w", padx=10)


# ==============================
    # EJECUCIÓN
# ==============================

if __name__ == "__main__":
    if tiene_password():
        login()
    else:
        crear_password()

