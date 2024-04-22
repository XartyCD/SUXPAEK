import tkinter as tk
from PIL import Image, ImageTk
import pygame
from auth_window import AuthWindow

root = None  # Глобальная переменная для объекта окна Tkinter

def play_background_music():
    pygame.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)  # -1 означает, что музыка будет проигрываться бесконечно

def main():
    global root  # Объявляем root как глобальную переменную
    root = tk.Tk()
    
    # Установить фоновое изображение
    img = Image.open("back.jpg")
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img)
    panel.place(x=0, y=0, relwidth=1, relheight=1)


    auth_window = AuthWindow(root)
    root.protocol("WM_DELETE_WINDOW", close_app)  # Вызывает функцию close_app при закрытии окна
    play_background_music()
    root.mainloop()

def close_app():
    pygame.mixer.music.stop()  # Останавливает музыку
    pygame.quit()  # Завершает pygame
    root.destroy()  # Закрывает окно tkinter

if __name__ == "__main__":
    main()