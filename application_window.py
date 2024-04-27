import tkinter as tk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window

class ApplicationWindow:
    def __init__(self,master,db,current_user,root):
        self.master = master
        self.root = root
        self.db = db
        self.current_user = current_user

        self.btn_logout = tk.Button(master,text = "Выйти",command=self.logout)
        self.btn_logout.pack()

        self.btn_statistics = tk.Button(master, text ="Статистика", command=self.open_statistics_window)
        self.btn_statistics.pack()

        self.btn_create_ticket = tk.Button(master, text="Создать заявку", command=self.create_ticket)
        self.btn_create_ticket.pack()


        self.search_frame= tk.Frame(master)
        self.search_frame.pack()

        self.search_label =tk.Label(self.search_frame, text="Поиск:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry =tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Найти", command = self.search_tickets)
        self.search_button.pack(side=tk.LEFT)

        self.label_ticket_info =tk.Label(master, text="")
        self.label_ticket_info.pack()

        self.label_user_info =tk.Label(master, text=f"Пользователь: {self.current_user}")
        self.label_user_info.pack()

        self.label_datetime =tk.Label(master, text="")
        self.label_datetime.pack()

        self.tickets_lables = []
        self.edit_buttons = []
        self.delete_buttons = []

        self.update_ticket_info()
        self.update_datetime()

    def create_ticket(self):
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")

        ticket_form = TicketForm(ticket_window, self.db, self, creation_time=current_datetime)

    def open_statistics_window(self):
        statistics_window.create_statistics_window(self.db)

    def edit_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Редактирование заявки")
        ticket_edit_form = TicketEditForm(ticket_window, self.db, ticket_id, self)

    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)
        self.update_ticket_info()

    def search_tickets(self):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)
        else:
            self.update_ticket_info()

    def display_search_results(self, tickets):
        for label in self.tickets_lables:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for button in self.delete_buttons:
            button.destroy()

        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.master, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.master, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(self.master, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.pack()
            self.delete_buttons.append(delete_button)

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска")
        else:
            self.label_ticket_info.config(text="Заявки не найдены")

    def update_ticket_info(self):
        self.remove_edit_buttons()
        self.remove_delete_buttons()

        for label in self.tickets_lables:
            label.destroy()

        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.master, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.master, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(self.master, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.pack()
            self.delete_buttons.append(delete_button)

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска")
        else:
            self.label_ticket_info.config(text="Заявки не найдены")
            

    def remove_edit_buttons(self):
        for button in self.edit_buttons:
            button.destroy()

    def remove_delete_buttons(self):
        for button in self.delete_buttons:
            button.destroy()
        self.delete_buttons = []

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self):
        self.master.destroy()
        self.root.deiconify()

        