import tkinter as tk
import datetime
import pygame
from tkinter import messagebox
from PIL import Image, ImageTk
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window

class ApplicationWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.master.title("Администрирование партией")

        master.geometry("900x650+440+300")
        master.resizable(False, False)  

        self.root = root
        self.db = db
        self.current_user = current_user

        self.img = Image.open("adminBack.png") 
        self.photo = ImageTk.PhotoImage(self.img)

        self.bg_label = tk.Label(self.master, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)
        self.render()


    def render(self):
        self.unlock_frame = tk.Frame(self.master, width=190, height=50, highlightbackground="#d46a06", highlightcolor="#d46a06", highlightthickness=4)
        self.unlock_frame.pack(padx=(0, 8), pady=(0, 4), side=tk.BOTTOM, anchor="se")


        self.unlock_title = tk.Label(self.unlock_frame, text="Смена темы", font=("Arial", 10))
        self.unlock_title.pack()
        self.unlock_button = tk.Button(self.unlock_frame, text="0 LVL", command=self.nullLevel)
        self.unlock_button.pack(side=tk.LEFT)
        self.unlock_button = tk.Button(self.unlock_frame, text="1 LVL", command=self.oneLevel)
        self.unlock_button.pack(side=tk.LEFT)
        self.unlock_button = tk.Button(self.unlock_frame, text="2 LVL", command=self.twoLevel)
        self.unlock_button.pack(side=tk.LEFT)
        self.unlock_button = tk.Button(self.unlock_frame, text="3 LVL", command=self.threeLevel)
        self.unlock_button.pack(side=tk.LEFT)
        self.unlock_buttonL = tk.Button(self.unlock_frame, text="none LVL", command=self.noneLevelL)
        self.unlock_buttonL.pack(side=tk.LEFT)
        self.unlock_buttonU = tk.Button(self.unlock_frame, text="none LVL", command=self.noneLevel)



        self.logout_frame = tk.Frame(self.master, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        self.logout_frame.pack(padx=(5, 0), pady=(5, 0), side=tk.LEFT, anchor="nw")

        self.logout_image = tk.PhotoImage(file="logout.png")
        self.logout_label = tk.Label(self.logout_frame, width=190, height=50, image=self.logout_image)
        self.logout_label.bind("<Button-1>", self.logout)
        self.logout_label.pack(pady=(5, 0))

        self.hide_btn = tk.Button(self.logout_frame, text="Скрыть лишнее", command=self.hideInterface, font=("Arial", 11))
        self.hide_btn.pack(pady=(10, 4))


        self.info_frame = tk.Frame(self.master, width=190, height=50, highlightbackground="#d46a06", highlightcolor="#d46a06", highlightthickness=4)
        self.info_frame.pack(padx=(0, 10), pady=(10, 0), side=tk.RIGHT, anchor="ne")

        self.label_user_info = tk.Label(self.info_frame, text=f"Приветствуем, Товарищ {self.current_user}!", wraplength=240, font=("Arial", 10))
        self.label_user_info.pack()

        self.label_datetime = tk.Label(self.info_frame, text="", font=("Arial", 10))
        self.label_datetime.pack(pady=(4, 0))

        self.navigate_frame = tk.Canvas(self.master, width=80, height=20, background=self.master["bg"])
        self.navigate_frame.pack(pady=(10, 0), anchor="n")

        self.btn_create_ticket = tk.Button(self.navigate_frame, text="Новая заявка", command=self.create_ticket, font=("Arial", 14))
        self.btn_create_ticket.pack(side=tk.LEFT, anchor="n")

        self.btn_statistics = tk.Button(self.navigate_frame, text="Аналитика", command=self.open_statistics_window, font=("Arial", 14))
        self.btn_statistics.pack(padx=(15, 0), side=tk.LEFT)

        self.search_frame= tk.Frame(self.master, width=230, height=40)
        self.search_frame.pack(pady=(12, 5))
        self.search_frame.pack_propagate(False)

        self.search_label = tk.Label(self.search_frame, text="Поиск:", font=("Arial", 12))
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame, width=28)
        self.search_entry.pack(side=tk.LEFT)

        self.search_entry.bind("<KeyRelease>", self.search_tickets)

        self.search_buttons = tk.Frame(self.master)
        self.search_buttons.pack(anchor="center")

        self.search_button = tk.Button(self.search_buttons, text="В ожидании", command=self.wait_search)
        self.search_button.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_buttons, text="В работе", command=self.work_search)
        self.search_button.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_buttons, text="Выполнено", command=self.finaly_search)
        self.search_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.master, text="Сброс", command=self.search_tickets, font=("Arial", 12))
        self.search_button.pack(anchor="center", pady=(4, 0))

        self.label_ticket_info = tk.Label(self.master, text="")
        self.label_ticket_info.pack(pady=(10, 0))

        self.canvas = tk.Canvas(self.master, width=240, height=390, highlightbackground="yellow", highlightcolor="yellow", highlightthickness=4)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.pack_propagate(False)

        self.ticketsContainer = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.ticketsContainer, anchor="n")

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(pady=(5, 0))
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.tickets_lables = []
        self.edit_buttons = []
        self.delete_buttons = []

        self.update_ticket_info()
        self.update_datetime()

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.master.bind_all("<MouseWheel>", self.scroll_canvas)


    def actualCount(self):
        tickets = self.db.get_all_tickets()
        if tickets:
            count = 0
            for ticket in tickets:
                if ticket[6] == "Выполнено":
                    count += 1
            return count
        else:
            return 0

    def nullLevel(self):
        count = self.actualCount()
        if count >= 0:
            self.update_background("adminBack.png")
            self.play_background_music("0lvl.mp3")

    def oneLevel(self):
        count = self.actualCount()
        if count >= 0:
            self.update_background("1lvl.png")
            self.play_background_music("1lvl.mp3")
        else: 
            self.update_background("adminBack.png")
            messagebox.showerror(f"Товарищ {self.current_user}!", f"Ты еще не достаточно опытен! Выполни еще {5 - count} заявки(-ок) (Требуется: {5})")
        
    def twoLevel(self):
        count = self.actualCount()
        if count >= 0:
            self.update_background("2lvl.png")
            self.play_background_music("2lvl.mp3")
        else: 
            self.update_background("adminBack.png")
            messagebox.showerror(f"Товарищ {self.current_user}!", f"Ты еще не достаточно опытен! Выполни еще {10 - count} заявки(-ок) (Требуется: {10})")
    
    def threeLevel(self):
        count = self.actualCount()
        if count >= 0:
            self.update_background("3lvl.png")
            self.play_background_music("3lvl.mp3")
        else: 
            self.update_background("adminBack.png")
            messagebox.showerror(f"Товарищ {self.current_user}!", f"Ты еще не достаточно опытен! Выполни еще {15 - count} заявки(-ок) (Требуется: {15})")

    def noneLevel(self):
        count = self.actualCount()
        if count >= 0:
            self.update_background("nonelvl.png")
            self.play_background_music("nonelvl.mp3")
        else: 
            self.update_background("adminBack.png")
            messagebox.showerror(f"Товарищ {self.current_user}!", f"Ты еще не достаточно опытен! Выполни еще {99 - count} заявки(-ок) (Требуется: {99})")
    
    def noneLevelL(self):
        messagebox.showerror(f"Товарищ {self.current_user}!", f"- Кнопка станет активной при вводе кодового слова!\n(Оно тебе не надо)")


    def play_background_music(self, music):
        pygame.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1) # -1 означает, что музыка будет проигрываться бесконечно

    def update_background(self, image_path):
        self.img = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.img)
        self.bg_label.config(image=self.photo)
        self.bg_label.image = self.photo


    def hideInterface(self):
        self.logout_frame.pack_forget()
        self.info_frame.pack_forget()
        self.navigate_frame.pack_forget()
        self.search_frame.pack_forget()
        self.search_buttons.pack_forget()
        self.search_button.pack_forget()
        self.label_ticket_info.pack_forget()
        self.canvas.pack_forget()
        self.hideRender()


    def seekInterface(self):
        self.logout_frame.pack(padx=(5, 0), pady=(5, 0), side=tk.LEFT, anchor="nw")
        self.logout_frame_hide.pack_forget()
        self.info_frame.pack(padx=(0, 10), pady=(10, 0), side=tk.RIGHT, anchor="ne")
        self.navigate_frame.pack(pady=(10, 0), anchor="n")
        self.search_frame.pack(pady=(12, 5))
        self.search_buttons.pack(anchor="center")
        self.search_button.pack(anchor="center", pady=(4, 0))
        self.label_ticket_info.pack(pady=(10, 0))
        self.canvas.pack(pady=(5, 0))
        self.update_ticket_info()


    def hideRender(self):
        self.logout_frame_hide = tk.Frame(self.master, highlightbackground="red", highlightcolor="red", highlightthickness=1)
        self.logout_frame_hide.pack(padx=(5, 0), pady=(5, 0), side=tk.LEFT, anchor="nw")

        self.logout_image_hide = tk.PhotoImage(file="logout.png")
        self.logout_label_hide = tk.Label(self.logout_frame_hide, width=190, height=50, image=self.logout_image_hide)
        self.logout_label_hide.bind("<Button-1>", self.logout)
        self.logout_label_hide.pack(pady=(5, 0))

        self.hide_btn = tk.Button(self.logout_frame_hide, text="Показать лишнее", command=self.seekInterface, font=("Arial", 11))
        self.hide_btn.pack(pady=(10, 4))




    def scroll_canvas(self, event):
        # Прокручиваем Canvas при помощи колесика мыши
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def create_ticket(self):
        blocker = 1
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Форма заявки")

        ticket_form = TicketForm(ticket_window, self.db, self)
        blocker = 0

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

    def search_tickets(self, event=None):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)
            if ((search_query == "вентилятор") or (search_query == "*~*") or (search_query == "nine")):
                self.unlock_buttonL.pack_forget()
                self.unlock_buttonU.pack(side=tk.LEFT)
            else:
                self.unlock_buttonL.pack()
                self.unlock_buttonU.pack_forget()
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

    def display_search_results(self, tickets):
        self.canvas.pack()
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
            label = tk.Label(self.ticketsContainer, wraplength=210, text=ticket_info)
            label.pack()
            self.tickets_lables.append(label)

            edit_button = tk.Button(self.ticketsContainer, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
            edit_button.pack()
            self.edit_buttons.append(edit_button)

            delete_button = tk.Button(self.ticketsContainer, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
            delete_button.pack()
            self.delete_buttons.append(delete_button)

        if tickets:
            self.label_ticket_info.config(text="Результаты поиска", font=("Arial", 12))
            self.canvas.pack(pady=(5, 0))
        else:
            self.label_ticket_info.config(text="Заявки не найдены", font=("Arial", 12))
            self.canvas.pack_forget()
            
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
            label = tk.Label(self.ticketsContainer, wraplength=210, text=ticket_info)
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
            self.label_ticket_info.config(text="Результаты поиска", font=("Arial", 12))
            self.canvas.pack(pady=(5, 0))
        else:
            self.label_ticket_info.config(text="Заявки не найдены", font=("Arial", 12))
            self.canvas.pack_forget()

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self, event=None):
        self.master.destroy()
        self.root.deiconify()
