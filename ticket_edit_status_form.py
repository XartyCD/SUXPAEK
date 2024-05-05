import tkinter as tk
from datetime import datetime

class TicketEditStatusForm:
    def __init__(self, master, db, ticket_id, parent_window):
        self.master = master
        self.db = db
        self.ticket_id = ticket_id
        self.parent_window = parent_window
        
        master.geometry("162x60+530+280")
        master.resizable(False, False)

        self.ticket_data = self.db.get_ticket_by_id(ticket_id)

        self.label_status = tk.Label(master, text="Статус:")
        self.label_status.grid(row=0, column=0, sticky="e")

        self.status_var = tk.StringVar(master)
        self.status_var.set(self.ticket_data[6])  # Устанавливаем текущий статус заявки
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=0, column=1)

        self.btn_submit = tk.Button(master, text="Сохранить", command=self.save)
        self.btn_submit.grid(row=1, columnspan=2)

    def save(self):
        ticket_data = {
            "equipment": self.ticket_data[2],  # Используем текущее значение equipment из self.ticket_data
            "fault_type": self.ticket_data[3],
            "problem_description": self.ticket_data[4],
            "client": self.ticket_data[5],
            "status": self.status_var.get(),
        # Другие поля, если есть
    }

        if ticket_data['status'] == "Выполнено":
            ticket_data['completion_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.update_ticket(self.ticket_id, ticket_data)
        self.parent_window.update_ticket_info()  # Добавляем вызов метода обновления отображения заявок
        self.master.destroy()



