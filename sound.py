import pygame

# Инициализация Pygame
pygame.init()

# Загрузка музыкального файла
pygame.mixer.music.load("music.mp3")

pygame.mixer.music.set_volume(0.5)  # пример установки громкости на 50%

pygame.mixer.music.play(-1)  # -1 означает повторять бесконечно, 1 означает воспроизвести один раз и так далее

pygame.mixer.music.stop()

# Освобождение ресурсов Pygame
pygame.quit()