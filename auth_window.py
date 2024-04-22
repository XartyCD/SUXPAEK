import tkinter as tk
from tkinter import messagebox
from database import Database
from application_window import ApplicationWindow
from special_window import SpecialWindow
from datetime import datetime 


class AuthWindow:

    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.db = Database("users.db")

        self.label_username = tk.Label(master, text = "имя пользователя: ")
        self.label_username.pack()

        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text = "пароль: ")
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show = "*")
        self.entry_password.pack()

        self.show_password_var = tk.BooleanVar()

        self.checkbox_show_password = tk.Checkbutton(master, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.checkbox_show_password.pack()

        self.btn_login = tk.Button(master, text = "Войти", command = self.login)
        self.btn_login.pack()

        self.label_datetime = tk.Label(master, text="")
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
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)
        application_window.title("Главное окно приложения")

        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = tk.Toplevel(self.master)
        special_window.title("Специальное окно для пользователя 2")

        special_window_instance = SpecialWindow(special_window, username, self, Database)

        tickets = self.db.get_all_tickets()
        special_window_instance.display_tickets(tickets)

    def update_datetime(self):
        current_datetime = datetime.now().strftime("%d.%n.%Y %H:%M:%S")
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.deiconify()
            
def main():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
