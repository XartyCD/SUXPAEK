import tkinter as tk
from tkinter import ttk
import datetime
from datetime import datetime
from collections import Counter

def create_statistics_window(db):
    global completedCount
    statistics_window = tk.Toplevel()
    statistics_window.title("Статистика")

    label_datetime = tk.Label(statistics_window, text="")
    label_datetime.pack()

    def update_datetime():
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        label_datetime.config(text=current_datetime)
        statistics_window.after(1000, update_datetime)
    update_datetime

    tree_tickets = ttk.Treeview(statistics_window)
    tree_tickets["columns"] = ("ID", "Оборудование", "Тип неисправности", "Описание", "Товарищ", "Статус", "Создание", "Выполнение", "Время выполнения")
    tree_tickets.heading("#0", text="№")
    tree_tickets.column("#0", anchor="w", width=50)
    for col in tree_tickets["columns"]:
        tree_tickets.heading(col, text=col)
        tree_tickets.column(col, anchor="w")
    tree_tickets.pack(expand=True, fill="both")

    tickets = db.get_all_tickets()
    if tickets:
        for ticket in tickets:
            if ticket[6] == "Выполнено" and ticket[7] and ticket[8]:
                creation_time = datetime.strptime(ticket[7], "%d.%m.%Y %H:%M:%S")
                complection_time = datetime.strptime(ticket[8], "%Y-%m-%d %H:%M:%S")
                execution_time = complection_time - creation_time
                execution_time_str = str(execution_time)
            else:
                execution_time_str = "Ещё не исполнено"
            tree_tickets.insert("", "end", text=ticket[1], values=tuple(ticket[1:])+(execution_time_str,))

    else:
         tree_tickets.insert("", "end", text="Нет данных", values=[""]*9)

    tree_fault_types = ttk.Treeview(statistics_window)
    tree_fault_types["columns"] = ("Тип неисправности", "Количество выполненных заявок")
    tree_fault_types.heading("#0", text="№")
    tree_fault_types.column("#0", anchor="w", width=50)
    for col in tree_fault_types["columns"]:
        tree_fault_types.heading(col, text=col)
        tree_fault_types.column(col, anchor="w")
    tree_fault_types.pack(expand=True, fill="both")

    tickets = db.get_all_tickets()

    if tickets:

        fault_type_counter = Counter()

        for ticket in tickets:
            if ticket[6] == "Выполнено":
                fault_type_counter[ticket[3]] += 1
                completedCount = fault_type_counter[ticket[3]]

        row_num = 1
        for fault_type, count in fault_type_counter.items():
            tree_fault_types.insert("", "end", text=row_num, values=(fault_type, count))
            row_num += 1
    else:
        tree_fault_types.insert("", "end", text="Нет данных", values=[""]*2)


        