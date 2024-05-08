import tkinter as tk
import pygame
from auth_window import AuthWindow
from tkinter import scrolledtext

def play_background_music():
    pygame.init()
    pygame.mixer.music.load('0lvl.mp3')
    pygame.mixer.music.play(-1) # -1 означает, что музыка будет проигрываться бесконечно

def main():
    global root 
    root = tk.Tk()

    auth_window = AuthWindow(root)
    root.protocol("WM_DELETE_WINDOW", close_app) # Вызывает функцию close_app при закрытии окна
    play_background_music()
    root.mainloop()

def close_app():
    root.destroy() # Закрывает окно tkinter

if __name__ == "__main__":
    main()