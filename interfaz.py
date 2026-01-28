import tkinter as tk
from tkinter import messagebox
import main
from tkinter import ttk
import matplotlib.pyplot as plt
from rules import EXPENSE_CATEGORIES
import hashlib
import os
from i18n import set_language, t
import locale



def language_selector():
    lang_win = tk.Tk()
    lang_win.title("Select language")
    lang_win.geometry("300x180")
    lang_win.resizable(False, False)

    tk.Label(
        lang_win,
        text="🌍 Select language / Seleccione idioma",
        font=("Arial", 11, "bold")
    ).pack(pady=15)

    def choose(lang):
        set_language(lang)
        lang_win.destroy()
        start_app()   # 👈 SOLO AQUÍ se crea la app

    tk.Button(
        lang_win,
        text="🇪🇸 Español",
        width=20,
        command=lambda: choose("es")
    ).pack(pady=5)

    tk.Button(
        lang_win,
        text="🇺🇸 English",
        width=20,
        command=lambda: choose("en")
    ).pack(pady=5)

    lang_win.mainloop()





def start():
    start_app()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


# ==============================
# HASH DE CONTRASEÑA
# ==============================
def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def has_password():
    data = main.load_data()
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

        data = main.load_data()  # ← NO crear dict nuevo
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
        data = main.load_data()

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

    # 🔄 Si la app ya existe (cambio de idioma), destruirla
    try:
        app_window.destroy()
    except:
        pass

    app_window = tk.Tk()
    app_window.title("🏛️ Finanzas de Babilonia")
    app_window.geometry("400x500")
    app_window.resizable(False, False)
    app_window.configure(bg=BG_COLOR)

    # --- TÍTULO ---
    title_label = tk.Label(
        app_window,
        text=t("menu_title"),
        font=("Arial", 16, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    )
    title_label.pack(pady=20)

    # --- SUBTÍTULO ---
    description_label = tk.Label(
        app_window,
        text=t("subtitle"),
        font=("Arial", 10),
        justify="center",
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    )
    description_label.pack(pady=10)

    # ✅ FRAME PRINCIPAL (OBLIGATORIO antes de usarlo)
    main_frame = tk.Frame(app_window, bg=BG_COLOR)
    main_frame.pack(pady=10)

    # --- BOTONES ---
    styled_button(
        main_frame,
        t("menu_register_income"),
        income_window
    ).pack(pady=8)

    styled_button(
        main_frame,
        t("menu_register_expense"),
        expense_window
    ).pack(pady=8)

    styled_button(
        main_frame,
        t("menu_view_report"),
        report_window
    ).pack(pady=8)

    styled_button(
        main_frame,
        t("menu_tools"),
        tools_window,
        SECONDARY_BUTTON_COLOR
    ).pack(pady=10)

    styled_button(
        app_window,
        t("exit"),
        app_window.quit,
        EXIT_COLOR
    ).pack(pady=30)

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
    tools_win.title(t("watch"))
    tools_win.geometry("380x450")
    tools_win.resizable(False, False)

    tk.Label(
        tools_win,
        text=t("watch"),
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
                messagebox.showerror(
                    t("error"),
                    t("must_enter_amount")
                )
                return

            amount_text = entry_amount.get().strip()

            try:
                amount = float(amount_text)
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números, sin puntos ni comas.")
                return

            has_debt = debt_var.get() == "si"
            pays_tithe = tithe_var.get() == "si"

            distribution = main.register_income_from_ui(
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
    win = tk.Toplevel()
    win.title("📊 Reporte financiero")
    win.geometry("360x450")
    win.resizable(False, False)
    win.configure(bg=BG_COLOR)

    data = main.load_data()
    incomes = data.get("income", [])
    expenses = data.get("expenses", [])

    # --- CÁLCULOS ---
    tithe = sum(i["distribucion"].get("tithe", 0) for i in incomes)
    debts = sum(i["distribucion"].get("debts", 0) for i in incomes)
    savings = sum(i["distribucion"].get("savings", 0) for i in incomes)

    # 💼 Gastos asignados desde ingresos
    expenses_assigned = sum(
        i["distribucion"].get("expenses", 0) for i in incomes
    )

    # 🧾 Gastos reales registrados
    expenses_used = sum(e.get("amount", 0) for e in expenses)

    # 💰 Disponible para gastar
    expenses_available = expenses_assigned - expenses_used

    # --- TÍTULO ---
    tk.Label(
        win,
        text="📊 REPORTE FINANCIERO",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    ).pack(pady=15)

    def report_line(label, value):
        frame = tk.Frame(win, bg=BG_COLOR)
        frame.pack(fill="x", padx=25, pady=4)

        tk.Label(
            frame,
            text=label,
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        ).pack(side="left")

        tk.Label(
            frame,
            text=f"${value:,.0f}",
            font=("Arial", 11, "bold"),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        ).pack(side="right")

    # --- MOSTRAR ---
    report_line("Diezmo:", tithe)
    report_line("Deudas:", debts)
    report_line("Ahorro (regla de Babilonia – 10%):", savings)
    report_line("Gastos disponibles:", expenses_available)

    ttk.Separator(win, orient="horizontal").pack(
        fill="x", padx=20, pady=15
    )

    styled_button(
        win,
        "🛠️ Herramientas financieras",
        tools_window,
        SECONDARY_BUTTON_COLOR
    ).pack(pady=8)

    styled_button(
        win,
        "Salir",
        win.destroy,
        EXIT_COLOR
    ).pack(pady=10)




def history_window():
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

        # 🟢 CASO 1: month es STRING → "2026-01"
        if isinstance(month, str):
            tk.Label(
                win,
                text=f"🗓️ {month}",
                font=("Arial", 11, "bold")
            ).pack(pady=5)
            continue

        # 🟢 CASO 2: month es DICT
        mes = month.get("mes", "Mes desconocido")

        tk.Label(
            win,
            text=f"🗓️ {mes}",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        resumen = month.get("resumen", {})

        for key, value in resumen.items():
            tk.Label(
                win,
                text=f"  {key}: ${value:,.0f}",
                anchor="w"
            ).pack(anchor="w")



def comparison_window():
    # Ventana para comparar meses
    try:
        ok = main.monthly_comparison_chart()

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
    history = main.get_history()

    # 🔒 Validación real
    if not isinstance(history, list) or len(history) < 2:
        messagebox.showinfo(
        "Gráfica mensual",
        "Se necesitan al menos 2 meses cerrados para mostrar la gráfica"
    )
        
        return

    try:
        months = []
        tithe = []
        debts = []
        savings = []
        expenses = []

        for m in history:
            # 🔐 Blindaje
            if not isinstance(m, dict):
                continue

            month_label = m.get("month", "Mes desconocido")
            summary = m.get("summary", {})

            months.append(month_label)
            tithe.append(summary.get("tithe", 0))
            debts.append(summary.get("debts", 0))
            savings.append(summary.get("savings", 0))
            expenses.append(summary.get("expenses", 0))

        if len(months) < 2:
            raise ValueError("Historial insuficiente")

        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(months, tithe, label="Diezmo")
        plt.plot(months, debts, label="Deudas")
        plt.plot(months, savings, label="Ahorro (Babilonia 10%)")
        plt.plot(months, expenses, label="Gastos")

        plt.title("Comparación mensual")
        plt.xlabel("Mes")
        plt.ylabel("Monto")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Ocurrió un problema al generar la gráfica:\n{e}",
            parent=tools_window
        )


def export_csv():
    # Exportar historial a CSV
    if main.exportar_historial_csv():
        messagebox.showinfo(
        "CSV",
        "No hay historial"
    )

    else:
        messagebox.showwarning(
        "CSV",
        "No hay historial para exportar"
    )



def analysis_window():
    # Ventana para mostrar análisis financiero
    message = main.analisis_financiero()

    messagebox.showinfo(
        "🧠 Análisis financiero",
        message
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
    language_selector()


