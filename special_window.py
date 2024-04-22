import tkinter as tk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm

from tkinter import *
from tkinter.ttk import *

class SpecialWindow:
    def __init__(self, master, username, auth_window, db):
        self.master = master
        self.username = username
        self.auth_window = auth_window  # Ссылка на окно авторизации
        self.db = db  # Ссылка на экземпляр базы данных

        self.label_welcome = tk.Label(master, text=f"Добро пожаловать, {username}!")
        self.label_welcome.pack()

        self.label_datetime = tk.Label(master, text="")
        self.label_datetime.pack()

        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.btn_search = tk.Button(master, text="Поиск", command=self.search_tickets_wrapper)
        self.btn_search.pack()

        self.btn_logout = tk.Button(master, text="Выйти", command=self.logout)
        self.btn_logout.pack()

        self.update_datetime()  # Начинаем обновление времени

        master.geometry('400x1000')
        master.resizable(0, 0)
        

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)  # Вызываем метод снова через 1000 мс (1 секунда)

    def display_tickets(self, tickets):
        for ticket in tickets:
            # Создаем виджеты для отображения информации о заявке
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:  # Проверяем, есть ли дата выполнения заявки
                ticket_info += f"\nДата выполнения: {ticket[8]}"
            label = tk.Label(self.master, text=ticket_info)
            label.pack()

            # Добавляем кнопку "Редактировать" для каждой заявки
            edit_button = tk.Button(self.master, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket_status(t))
            edit_button.pack()

    def update_tickets_display(self):
        # Очищаем текущее отображение заявок, кроме приветственного сообщения и имени пользователя
        for widget in self.master.winfo_children():
            if widget not in (self.label_welcome, self.label_datetime, self.search_entry, self.btn_search, self.btn_logout):
                widget.destroy()

        tickets = self.db.get_all_tickets()

        # Отображаем заявки
        self.display_tickets(tickets)

    def search_tickets_wrapper(self):
        search_query = self.search_entry.get()
        tickets = self.db.search_tickets(search_query)
        self.update_tickets_display(tickets)

    def edit_ticket_status(self, ticket_id):
        # Открываем окно изменения статуса заявки
        ticket_edit_status_window = tk.Toplevel(self.master)
        ticket_edit_status_window.title("Изменение статуса заявки")
        ticket_edit_status_form = TicketEditStatusForm(ticket_edit_status_window, self.db, ticket_id, self)

    def logout(self):
        self.master.destroy()  
        self.auth_window.show()
