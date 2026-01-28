import tkinter as tk
from tkinter import simpledialog, messagebox
from main import register_income
from i18n import t  # si usas traducciones



def register_income_gui():
    messagebox.showinfo("Info", "Registrar ingreso (pendiente)")

def register_expense_gui():
    messagebox.showinfo("Info", "Registrar gasto (pendiente)")

def create_goal_gui():
    messagebox.showinfo("Info", "Crear meta (pendiente)")

def contribute_goal_gui():
    messagebox.showinfo("Info", "Aportar a meta (pendiente)")

def view_report_gui():
    messagebox.showinfo("Info", "Reporte financiero (pendiente)")

def expenses_chart_gui():
    messagebox.showinfo("Info", "Gráfica de gastos (pendiente)")

def goals_chart_gui():
    messagebox.showinfo("Info", "Gráfica de metas (pendiente)")

def reset_data_gui():
    messagebox.showwarning("Advertencia", "Reinicio de datos (pendiente)")




# 1️⃣ Funciones (primero)
def register_income_gui():
    try:
        amount = simpledialog.askfloat(
            t("income_title"),
            t("enter_income_amount")
        )
        if amount is None:
            return

        has_debts = messagebox.askyesno(
            t("has_debts_title"),
            t("has_debts")
        )

        pay_tithe = messagebox.askyesno(
            t("pay_tithe_title"),
            t("pay_tithe")
        )

        distribution = register_income(amount, has_debts, pay_tithe)

        messagebox.showinfo(
            t("success"),
            f"{t('income_registered')}\n\n"
            f"{t('savings_babylon_label')}: ${distribution['savings']:,.0f}\n"
            f"{t('expenses_label')}: ${distribution['expenses']:,.0f}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# 2️⃣ Crear ventana (DESPUÉS de las funciones)
root = tk.Tk()
root.title("🏛️ Finanzas de Babilonia")
root.geometry("400x300")


frame = tk.Frame(root)
frame.pack(pady=20)



tk.Button(frame, text="Registrar ingreso", width=30, command=register_income_gui).pack(pady=4)
tk.Button(frame, text="Registrar gasto", width=30, command=register_expense_gui).pack(pady=4)
tk.Button(frame, text="Crear meta financiera", width=30, command=create_goal_gui).pack(pady=4)
tk.Button(frame, text="Aportar a meta", width=30, command=contribute_goal_gui).pack(pady=4)
tk.Button(frame, text="Ver reporte financiero", width=30, command=view_report_gui).pack(pady=4)
tk.Button(frame, text="Gráfica de gastos", width=30, command=expenses_chart_gui).pack(pady=4)
tk.Button(frame, text="Gráfica de metas", width=30, command=goals_chart_gui).pack(pady=4)
tk.Button(frame, text="Reiniciar datos", width=30, command=reset_data_gui).pack(pady=4)

tk.Button(frame, text="Salir", width=30, command=root.quit).pack(pady=10)



# 4️⃣ Main loop (SIEMPRE al final)
root.mainloop()

