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
        master.resizable(False, False)  

        self.img = Image.open("adminBack.png") 
        self.photo = ImageTk.PhotoImage(self.img)

        self.bg_label = tk.Label(self.master, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.root = root
        self.db = db
        self.current_user = current_user

        self.logout_image = tk.PhotoImage(file="logout.png")
        self.logout_label = tk.Label(master, width=190, height=50, image=self.logout_image)
        self.logout_label.bind("<Button-1>", self.logout)
        self.logout_label.pack(padx=(10, 0), pady=(10, 0), side=tk.LEFT, anchor="nw")

        self.info_frame = tk.Frame(master, width=190, height=50, highlightbackground="#d46a06", highlightcolor="#d46a06", highlightthickness=4)
        self.info_frame.pack(padx=(0, 10), pady=(10, 0), side=tk.RIGHT, anchor="ne")

        self.label_user_info = tk.Label(self.info_frame, text=f"Приветствуем, Товарищ 111111!", wraplength=240, font=("Arial", 10))
        self.label_user_info.pack()

        self.label_datetime = tk.Label(self.info_frame, text="", font=("Arial", 10))
        self.label_datetime.pack(pady=(4, 0))

        self.navigate_frame = tk.Canvas(master, width=80, height=20, background=master["bg"])
        self.navigate_frame.pack(pady=(15, 0), anchor="n")

        self.btn_create_ticket = tk.Button(self.navigate_frame, text="Новая заявка", command=self.create_ticket, font=("Arial", 14))
        self.btn_create_ticket.pack(side=tk.LEFT, anchor="n")

        self.btn_statistics = tk.Button(self.navigate_frame, text="Аналитика", command=self.open_statistics_window, font=("Arial", 14))
        self.btn_statistics.pack(padx=(15, 0), side=tk.LEFT)

        self.search_frame= tk.Frame(master)
        self.search_frame.pack()

        self.search_label = tk.Label(self.search_frame, text="Поиск:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Найти", command=self.search_tickets)
        self.search_button.pack(side=tk.LEFT)

        self.label_ticket_info = tk.Label(master, text="")
        self.label_ticket_info.pack()

        self.canvas = tk.Canvas(master, highlightbackground="yellow", highlightcolor="yellow", highlightthickness=4)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)

        # Создаем фрейм для содержимого
        self.ticketsContainer = tk.Frame(self.canvas)

        # Создаем окно для фрейма в Canvas
        self.canvas.create_window(0, 0, window=self.ticketsContainer, anchor="n")  # Anchor "n" для центрирования по вертикали

        # Привязываем обновление размеров Canvas к обновлению размеров содержимого
        self.ticketsContainer.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Привязываем скроллбар к Canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Упаковываем Canvas и скроллбар
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.tickets_lables = []
        self.edit_buttons = []
        self.delete_buttons = []

        self.update_ticket_info()
        self.update_datetime()

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.master.bind_all("<MouseWheel>", self.scroll_canvas)

    def scroll_canvas(self, event):
        # Прокручиваем Canvas при помощи колесика мыши
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def create_ticket(self):
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")

        ticket_form = TicketForm(ticket_window, self.db, self)

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
        self.ticketsContainer.pack()
        for label in self.tickets_lables:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for button in self.delete_buttons:
            button.destroy()

        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nТоварищ: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.ticketsContainer, wraplength=160, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.ticketsContainer, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(self.ticketsContainer, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.pack()
            self.delete_buttons.append(delete_button)

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска")
        else:
            self.label_ticket_info.config(text="Заявки не найдены")
            self.ticketsContainer.pack_forget()

    def update_ticket_info(self):
        for label in self.tickets_lables:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for button in self.delete_buttons:
            button.destroy()

        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nТоварищ: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.ticketsContainer, wraplength=160, text=ticket_info, font=("Arial", 10))
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.ticketsContainer, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(self.ticketsContainer, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.pack()
            self.delete_buttons.append(delete_button)

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска")
        else:
            self.label_ticket_info.config(text="Заявки не найдены")

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self, event=None):
        self.master.destroy()
        self.root.deiconify()
