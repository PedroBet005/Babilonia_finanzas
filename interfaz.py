
import tkinter as tk
from tkinter import messagebox
import main
from tkinter import ttk
import matplotlib.pyplot as plt
from rules import EXPENSE_CATEGORIES
import hashlib
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


# ==============================
# HASH DE CONTRASEÑA
# ==============================
def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def has_password():
    data = main.cargar_datos()
    return "password_hash" in data


def create_password():
    pw_window = tk.Tk()
    pw_window.title("Crear contraseña - Babilonia Finanzas")
    pw_window.geometry("300x150")

    tk.Label(pw_window, text="Crea tu contraseña").pack(pady=5)
    pw_entry = tk.Entry(pw_window, show="*")
    pw_entry.pack(pady=5)

    def save_pw():
        password = pw_entry.get()
        if password == "":
            messagebox.showerror("Error", "La contraseña no puede estar vacía")
            return

        data = main.cargar_datos()  # ← NO crear dict nuevo
        data["password_hash"] = generate_hash(password)
        main.guardar_datos(data)

        messagebox.showinfo("Éxito", "Contraseña creada correctamente")
        pw_window.destroy()
        start_app()

    tk.Button(pw_window, text="Guardar", command=save_pw).pack(pady=10)
    pw_window.mainloop()


def login():
    login_window = tk.Tk()
    login_window.title("Acceso - Babilonia Finanzas")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Ingresa tu contraseña").pack(pady=5)
    pw_entry = tk.Entry(login_window, show="*")
    pw_entry.pack(pady=5)

    def validate_pw():
        password = pw_entry.get()
        data = main.cargar_datos()

        if generate_hash(password) == data["password_hash"]:
            login_window.destroy()
            start_app()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    tk.Button(login_window, text="Entrar", command=validate_pw).pack(pady=10)
    login_window.mainloop()


# ==============================
# COLORES
# ==============================
BG_COLOR = "#f4f6f7"
PRIMARY_COLOR = "#2c3e50"
BUTTON_COLOR = "#34495e"
SECONDARY_BUTTON_COLOR = "#5dade2"
EXIT_COLOR = "#c0392b"
TEXT_COLOR = "white"


# ==============================
# CONFIGURACIÓN DE LA VENTANA
# ==============================
def start_app():
    global app_window
    app_window = tk.Tk()
    app_window.title("🏛️ Finanzas de Babilonia")
    app_window.geometry("400x500")
    app_window.resizable(False, False)
    app_window.configure(bg=BG_COLOR)

    # --- TÍTULO ---
    title_label = tk.Label(
        app_window,
        text="FINANZAS DE BABILONIA",
        font=("Arial", 16, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    )
    title_label.pack(pady=20)

    # --- TEXTO INFORMATIVO ---
    description_label = tk.Label(
        app_window,
        text="Aplicación de finanzas personales\nbasada en principios de Babilonia",
        font=("Arial", 10),
        justify="center",
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    )
    description_label.pack(pady=10)

    # --- FRAME PRINCIPAL (botones visibles) ---
    main_frame = tk.Frame(app_window)
    main_frame.pack(pady=10)

    # --- BOTONES (CON FUNCIÓN) ---
    styled_button(main_frame, "Registrar ingreso", income_window).pack(pady=8)
    styled_button(main_frame, "Registrar gasto", expense_window).pack(pady=8)
    styled_button(main_frame, "Ver reporte", report_window).pack(pady=8)
    styled_button(
        main_frame,
        "📊 Herramientas financieras",
        tools_window,
        SECONDARY_BUTTON_COLOR
    ).pack(pady=10)
    styled_button(app_window, "Salir", app_window.quit, EXIT_COLOR).pack(pady=30)

    app_window.mainloop()


def styled_button(parent, text, command, color=BUTTON_COLOR):
    return tk.Button(
        parent,
        text=text,
        width=25,
        bg=color,
        fg=TEXT_COLOR,
        activebackground="#1f618d",
        relief="flat",
        command=command
    )


def tools_window():
    global tools_win
    tools_win = tk.Toplevel()
    tools_win.configure(bg=BG_COLOR)
    tools_win.transient(app_window)      # pertenece a la ventana principal
    tools_win.grab_set()                 # bloquea la ventana principal
    tools_win.title("📊 Herramientas financieras")
    tools_win.geometry("380x450")
    tools_win.resizable(False, False)

    tk.Label(
        tools_win,
        text="Herramientas financieras",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    ).pack(pady=15)

    tk.Button(
        tools_win, 
        text="Ver historial mensual", 
        width=30, 
        command=history_window
    ).pack(pady=8)

    tk.Button(
        tools_win, 
        text="Comparar meses", 
        width=30, 
        command=comparison_window
    ).pack(pady=8)

    tk.Button(
        tools_win, 
        text="Ver alertas", 
        width=30, 
        command=alerts_window
    ).pack(pady=8)

    tk.Button(
        tools_win, 
        text="📈 Ver gráfica mensual", 
        width=30, 
        command=monthly_chart_window
    ).pack(pady=8)

    tk.Button(
        tools_win, 
        text="💾 Exportar historial CSV", 
        width=30, 
        command=export_csv
    ).pack(pady=8)

    tk.Button(
        tools_win, 
        text="🧠 Análisis financiero", 
        width=30, 
        command=analysis_window
    ).pack(pady=8)
    tk.Button(
        tools_win, 
        text="Cerrar", 
        width=30, command=tools_win.destroy
    ).pack(pady=20)



def income_window():
    # Ventana para registrar ingresos
    win = tk.Toplevel()
    win.title("Registrar ingreso")

    tk.Label(win, text="Monto del ingreso").pack(pady=5)
    entry_amount = tk.Entry(win)
    entry_amount.pack(pady=5)

    tk.Label(win, text="¿Tiene deudas?").pack(pady=5)
    debt_var = tk.StringVar(value="no")

    tk.Radiobutton(win, text="Sí", variable=debt_var, value="si").pack()
    tk.Radiobutton(win, text="No", variable=debt_var, value="no").pack()

    tk.Label(win, text="¿Desea pagar diezmo?").pack(pady=5)
    tithe_var = tk.StringVar(value="no")

    tk.Radiobutton(win, text="Sí", variable=tithe_var, value="si").pack()
    tk.Radiobutton(win, text="No", variable=tithe_var, value="no").pack()

    result_frame = tk.Frame(win)
    result_frame.pack(pady=10)

    def save_income():
        # Limpiar resultados previos
        for widget in result_frame.winfo_children():
            widget.destroy()

        try:
            if not entry_amount.get().strip():
                messagebox.showerror("Error", "Debe ingresar un monto")
                return

            amount_text = entry_amount.get().strip()

            try:
                amount = float(amount_text)
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números, sin puntos ni comas.")
                return

            has_debt = debt_var.get() == "si"
            pays_tithe = tithe_var.get() == "si"

            distribution = main.registrar_ingreso_desde_ui(
                amount,
                has_debt,
                pays_tithe
            )

            if distribution is None:
                messagebox.showwarning(
                    "Ingreso no guardado",
                    "⚠️ El período financiero está cerrado.\nNo se pueden registrar ingresos."
                )
                return

            tk.Label(result_frame, text="📊 Distribución del ingreso", font=("Arial", 12, "bold")).pack()

            for key, value in distribution.items():
                tk.Label(result_frame, text=f"{key}: ${value:,.0f}").pack()

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
        command=save_income
    ).pack(pady=10)


def expense_window():
    # Ventana para registrar gastos
    win = tk.Toplevel()
    win.title("Registrar gasto")

    tk.Label(win, text="Monto del gasto").pack()
    entry_amount = tk.Entry(win)
    entry_amount.pack(pady=5)

    category_var = tk.StringVar(value=EXPENSE_CATEGORIES[0])

    tk.Label(win, text="Categoría").pack()
    tk.OptionMenu(win, category_var, *EXPENSE_CATEGORIES).pack(pady=5)

    entry_other = tk.Entry(win)
    entry_other.pack(pady=5)
    entry_other.pack_forget()

    def on_category_change(*args):
        if category_var.get() == "Otros":
            entry_other.pack()
        else:
            entry_other.pack_forget()

    category_var.trace_add("write", on_category_change)

    def save_expense():
        try:
            if not entry_amount.get().strip():
                messagebox.showerror("Error", "Debe ingresar un monto")
                return

            amount = float(entry_amount.get())
            if amount <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return

            category = category_var.get()

            if category == "Otros":
                category = entry_other.get().strip()
                if not category:
                    messagebox.showerror("Error", "Ingrese el nombre del gasto")
                    return

            success = main.registrar_gasto_desde_ui(amount, category)

            if not success:
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
        command=save_expense
    ).pack(pady=10)


def report_window():
    # Ventana para mostrar reporte mensual
    win = tk.Toplevel()
    win.title("📊 Reporte mensual")

    report = main.obtener_reporte_mensual()
    month_status = "Abierto" if main.obtener_estado_mes() else "Cerrado"

    if not report:
        tk.Label(
            win,
            text="No hay datos disponibles para mostrar.",
            fg="red"
        ).pack(pady=10)
        return

    tk.Label(
        win,
        text=f"Mes abierto o cerrado: {month_status}",
        font=("Arial", 10, "italic")
    ).pack(pady=5)

    # ─── Orden correcto del reporte ───
    report_order = [
        "Diezmo",
        "Mi pago",
        "Mi pago disponible",
        "Ahorro emergencia",
        "Ahorro general",
        "Ahorro total",
        "Deudas",
        "Gastos"
    ]

    for key in report_order:
        value = report.get(key, 0)
        tk.Label(
            win,
            text=f"{key}: ${value:,.0f}",
            anchor="w"
        ).pack(fill="x")

    tk.Button(
        win,
        text="Cerrar",
        command=win.destroy
    ).pack(pady=10)




def history_window():    
    # Ventana para mostrar historial mensual
    win = tk.Toplevel()
    win.title("📚 Historial mensual")
    win.transient()
    win.grab_set()
    win.focus_force()

    history = main.obtener_historial()

    def close_window():
        win.grab_release()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", close_window)

    if not history:
        tk.Label(
            win,
            text="📭 No hay meses cerrados aún",
            font=("Arial", 11, "italic")
        ).pack(pady=10)

        win.after(0, lambda: win.grab_release())
        return

    for month in history:
        tk.Label(
            win,
            text=f"🗓️ {month['mes']}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        for key, value in month["resumen"].items():
            tk.Label(win, text=f"  {key}: ${value:,.0f}").pack(anchor="w")


def comparison_window():
    # Ventana para comparar meses
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


def monthly_chart_window():
    # Ventana para mostrar gráfica mensual
    history = main.obtener_historial_para_grafica()

    if len(history) < 2:
        messagebox.showinfo(
            "Gráfica",
            "Se necesitan al menos 2 meses cerrados para mostrar la gráfica"
        )
        return

    months = [m["mes"] for m in history]
    expenses = [m["resumen"].get("Gastos", 0) for m in history]
    savings = [m["resumen"].get("Ahorro total", 0) for m in history]

    plt.figure()
    plt.plot(months, expenses, label="Gastos")
    plt.plot(months, savings, label="Ahorro total")
    plt.title("Evolución financiera mensual")
    plt.xlabel("Mes")
    plt.ylabel("Monto ($)")
    plt.legend()

    plt.gcf().canvas.manager.window.attributes('-topmost', 1)
    plt.gcf().canvas.manager.window.attributes('-topmost', 0)

    plt.show()


def export_csv():
    # Exportar historial a CSV
    if main.exportar_historial_csv():
        messagebox.showinfo(
            "CSV",
            "Historial exportado correctamente",
            parent=tools_window
        )
    else:
        messagebox.showwarning(
            "CSV",
            "No hay historial para exportar",
            parent=tools_window
        )


def analysis_window():
    # Ventana para mostrar análisis financiero
    message = main.analisis_financiero()

    messagebox.showinfo(
        "🧠 Análisis financiero",
        message,
        parent=tools_window
    )


def alerts_window():
    # Ventana para mostrar alertas financieras
    win = tk.Toplevel()
    win.title("🔔 Alertas financieras")
    win.transient()
    win.grab_set()
    win.focus_force()

    def close_window():
        win.grab_release()
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", close_window)

    alerts = main.analizar_alertas()

    if not alerts:
        tk.Label(win, text="✅ No hay alertas. Buen trabajo 👏").pack(pady=10)
        win.after(0, lambda: win.grab_release())
        return

    for alert in alerts:
        tk.Label(win, text=alert, fg="red").pack(anchor="w", padx=10)


# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":
    if has_password():
        login()
    else:
        create_password()
