import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from database import Database
from application_window import ApplicationWindow
from special_window import SpecialWindow
import datetime


class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.master.configure(bg="#700202")
        self.db = Database("users.db")

        self.exit_button = tk.Button(self.master, width=18, text="Выйти из партии", command=self.emergency_exit, background="red", activebackground="#d90000", 
                                    foreground="white", activeforeground="white", font=("Arial", 14))

        self.exit_button.pack(pady=(23, 0))

        master.geometry("800x560+1100+300")
        master.resizable(False, False)  #Запрет масштабирования окна

        self.img = Image.open("authBack.jpg") # Создаем изображение
        self.photo = ImageTk.PhotoImage(self.img)

        self.authcontainer = tk.Frame(master, width=570, height=371, highlightbackground="#d46a06", highlightcolor="#d46a06", highlightthickness=4)  # Создаем контейнер с элементами внутри
        self.authcontainer.pack(pady=(37, 0), anchor="center")  # два параметра high для цвета при клике на ввод и для обычного поведения
        self.authcontainer.pack_propagate(False)
        
        self.bg_label = tk.Label(self.authcontainer, image=self.photo)
        self.bg_label.place(relwidth=1, relheight=1)


        self.label_username = tk.Label(self.authcontainer, text = "Логин: ",  background="gold", font=("Arial", 18))
        self.label_username.pack(pady=(60, 3))

        self.entry_username = tk.Entry(self.authcontainer, width=30)
        self.entry_username.pack(pady=(0, 17))

        self.label_password = tk.Label(self.authcontainer, text = "Пароль: ", background="gold", font=("Arial", 18))
        self.label_password.pack(pady=(0, 3))

        self.entry_password = tk.Entry(self.authcontainer, show = "🤐", width=30)
        self.entry_password.pack(pady=(0, 1))

        self.show_password_var = tk.BooleanVar()

        self.checkbox_show_password = tk.Checkbutton(self.authcontainer, text="Показать пароль", font=("Arial", 12), 
                                                        variable=self.show_password_var, command=self.toggle_password_visibility,
                                                        background="orange", activebackground="orange")
        self.checkbox_show_password.pack(pady=(0, 23))

        self.btn_login = tk.Button(self.authcontainer, width=9, text = "Вступить", command = self.login, 
                                    background="yellow", activebackground="#c4be00", font=("Arial", 14))
                                    
        self.btn_login.pack()

        self.label_datetime = tk.Label(self.authcontainer, width=19, height=2, text="", background="#700909", highlightbackground="white", highlightthickness=2, font=("Arial", 14))
        self.label_datetime.pack(pady=(0, 0), expand=True, anchor="s")

        self.label_datetime.pack()

        self.update_datetime()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.check_credentials(username, password):
            self.master.withdraw()
            if username == "2":
                self.open_special_window(username)
            else:
                self.open_application_window(username)
        elif (username == "" and password == ""):
            messagebox.showerror("ОДУМАЙТЕСЬ!", "Товарищ! Вы забыли ввести свои данные!")
        else:
            messagebox.showerror("ВЫ АРЕСТОВАНЫ!", "Введененные вами данные не соответствуют сводкам КГБ")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="🤐")

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)

        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = tk.Toplevel(self.master)
        special_window.title("Специальное окно для пользователя 2")

        special_window_instance = SpecialWindow(special_window, username, self, Database)

        tickets = self.db.get_all_tickets()
        special_window_instance.display_tickets(tickets)

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.deiconify()

    def emergency_exit(self):
        self.master.destroy()
            
def main():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
