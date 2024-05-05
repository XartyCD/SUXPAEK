import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm

class SpecialWindow:
    def __init__(self, master, username, auth_window, db):
        self.master = master
        self.username = username
        self.master.title("Меню помогающего Товарища")

        master.geometry("570x780+490+200")
        master.resizable(False, False) 


        self.img = Image.open("specBack.png") 
        self.photo = ImageTk.PhotoImage(self.img)

        self.bg_label = tk.Label(self.master, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.root = auth_window
        self.db = db
        self.current_user = username

        

        self.info_frame = tk.Frame(master, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.info_frame.pack(pady=(10, 0), padx=(10, 0), side=tk.LEFT, anchor="nw")

        self.label_user_info = tk.Label(self.info_frame, text=f"Приветствуем, Товарищ {self.username}!", wraplength=240, font=("Arial", 10))
        self.label_user_info.pack()

        self.label_datetime = tk.Label(self.info_frame, text="", font=("Arial", 10))
        self.label_datetime.pack(pady=(4, 0))

        self.logout_image = tk.PhotoImage(file="specLogout.png")
        self.logout_label = tk.Label(self.info_frame, width=140, height=40, image=self.logout_image)
        self.logout_label.bind("<Button-1>", self.logout)
        self.logout_label.pack(pady=(17, 8))


        self.search = tk.Frame(master, width=230, height=23)
        self.search.pack(pady=(20, 5))
        self.search.pack_propagate(False)

        self.search_frame = tk.Frame(self.search)
        self.search_frame.pack()

        self.search_label = tk.Label(self.search_frame, text="Поиск:", font=("Arial", 12))
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame, width=28)
        self.search_entry.pack(side=tk.LEFT)

        self.search_entry.bind("<KeyRelease>", self.search_tickets)

        self.search_buttons = tk.Frame(master)
        self.search_buttons.pack(anchor="center")

        
        self.search_button = tk.Button(self.search_buttons, text="В ожидании", command = self.wait_search)
        self.search_button.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_buttons, text="В работе", command = self.work_search)
        self.search_button.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_buttons, text="Выполнено", command = self.finaly_search)
        self.search_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(master, text="Сброс", command = self.search_tickets, font=("Arial", 12))
        self.search_button.pack(anchor="center", pady=(4, 0))

        self.label_ticket_info = tk.Label(master, text="")
        self.label_ticket_info.pack(pady=(10, 0))

        self.canvas = tk.Canvas(master, width=240, height=490, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.pack_propagate(False)

        # Создаем фрейм для содержимого
        self.ticketsContainer = tk.Frame(self.canvas)

        # Создаем окно для фрейма в Canvas
        self.canvas.create_window(0, 0, window=self.ticketsContainer, anchor="n")  # Anchor "n" для центрирования по вертикали

        # Привязываем скроллбар к Canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Упаковываем Canvas и скроллбар
        self.canvas.pack(pady=(5, 0))
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

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)  # Вызываем метод снова через 1000 мс (1 секунда)
        

    def display_search_results(self, tickets):
        self.canvas.pack()
        for label in self.tickets_lables:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nТоварищ: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.ticketsContainer, wraplength=210, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.ticketsContainer, text="Изменить статус", command=lambda t=ticket[0]: self.edit_ticket_status(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)


        if tickets:
            self.label_ticket_info.config(text="Результаты поиска", font=("Arial", 12))
            self.canvas.pack(pady=(5, 0))
        else:
            self.label_ticket_info.config(text="Заявки не найдены", font=("Arial", 12))
            self.canvas.pack_forget()
            
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def search_tickets(self, event=None):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)
        else:
            self.update_ticket_info()

    def wait_search(self):
        search_query = "В ожидании"
        tickets = self.db.search_tickets(search_query)
        self.display_search_results(tickets)

    def work_search(self):
        search_query = "В работе"
        tickets = self.db.search_tickets(search_query)
        self.display_search_results(tickets)
    
    def finaly_search(self):
        search_query = "Выполнено"
        tickets = self.db.search_tickets(search_query)
        self.display_search_results(tickets)



    def update_ticket_info(self):
        for label in self.tickets_lables:
            label.destroy()

        for button in self.edit_buttons:
            button.destroy()

        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nТоварищ: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            label = tk.Label(self.ticketsContainer, wraplength=210, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.ticketsContainer, text="Изменить статус", command=lambda t=ticket[0]: self.edit_ticket_status(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска", font=("Arial", 12))
            self.canvas.pack(pady=(5, 0))
        else:
            self.label_ticket_info.config(text="Заявки не найдены", font=("Arial", 12))
            self.canvas.pack_forget()

    def edit_ticket_status(self, ticket_id):
        # Открываем окно изменения статуса заявки
        ticket_edit_status_window = tk.Toplevel(self.master)
        ticket_edit_status_window.title("Изменение статуса заявки")
        ticket_edit_status_form = TicketEditStatusForm(ticket_edit_status_window, self.db, ticket_id, self)

    def logout(self, event=None):
        self.master.destroy()  
        self.root.show()



    
