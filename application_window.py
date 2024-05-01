import tkinter as tk
import datetime
from PIL import Image, ImageTk
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window

class ApplicationWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.master.title("Администрирование партией")

        master.geometry("900x650+600+300")
        master.resizable(False, False)  #Запрет масштабирования окна

        self.img = Image.open("adminBack.png") # Создаем изображение
        self.photo = ImageTk.PhotoImage(self.img)

        self.bg_label = tk.Label(self.master, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.root = root
        self.db = db
        self.current_user = current_user


        self.logout_image = tk.PhotoImage(file="logout.png")
        self.logout_label = tk.Label(master, width=190, height=50, image=self.logout_image)
        self.logout_label.bind("<Button-1>", self.logout)
        self.logout_label.pack(padx=(10, 0), pady=(10, 0), anchor="nw")


        self.navigate_frame = tk.Frame(master, width=570, height=371, highlightbackground="#d46a06", highlightcolor="#d46a06", highlightthickness=4)
        self.navigate_frame.pack()

        self.btn_statistics = tk.Button(self.navigate_frame, text ="Аналитика", command=self.open_statistics_window)
        self.btn_statistics.pack(side=tk.LEFT)

        self.btn_create_ticket = tk.Button(self.navigate_frame, text="Новая заявка", command=self.create_ticket)
        self.btn_create_ticket.pack(side=tk.LEFT)


        self.search_frame= tk.Frame(master)
        self.search_frame.pack()

        self.search_label = tk.Label(self.search_frame, text="Поиск:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Найти", command = self.search_tickets)
        self.search_button.pack(side=tk.LEFT)

        self.label_ticket_info = tk.Label(master, text="")
        self.label_ticket_info.pack()

        self.label_user_info = tk.Label(master, text=f"Пользователь: {self.current_user}")
        self.label_user_info.pack()

        self.label_datetime = tk.Label(master, text="")
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
            label = tk.Label(self.master, text=ticket_info, wraplength=55) #редактирование контейнера каждой заявки
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

    def logout(self, event=None):
        self.master.destroy()
        self.root.deiconify()

        