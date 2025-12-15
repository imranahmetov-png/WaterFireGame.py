import time
import pygame
import sys
import turtle

# НАСТРОЙКИ
pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fire and Water")
clock = pygame.time.Clock()
FPS = 60

# ЦВЕТА
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
BLUE = (60, 120, 220)
GRAY = (160, 160, 160)
ORANGE = (255, 120, 0)
CYAN = (0, 200, 200)
GREEN = (0, 200, 0)
# ШРИФТ
font = pygame.font.SysFont("arial", 24)

# СТАРТОВЫЕ ПОЗИЦИИ
FIRE_START = (100, 135)
WATER_START = (1050, 540)
# ТАЙМЕР
start_time = pygame.time.get_ticks() # время начала игры
final_time = None  # финальное время (после победы)

# Платформы и преграды
walls = [
    pygame.Rect(0, 580, 1200, 20),  # это пол
    pygame.Rect(100, 475, 1100, 20),  # платформа 2
    pygame.Rect(0, 175, 1100, 20),   # верхняя платформа
    pygame.Rect(0, 70, 1200, 20), # платформа 2 с верху вниз
    pygame.Rect(100,275,1100,20), # платформа 3 с верху вниз
    pygame.Rect(0,375,1100,20), # платформа 4 с верху вниз
    pygame.Rect(800,440,150,40), # препятствие на платформе 2
    pygame.Rect(600,250,70,30), # препятствие на платформе 3
    pygame.Rect(200,140,70,40), # препятствие на верхней платформе 1
    pygame.Rect(800,140,90,40), # препятствие на верхней платформе 2
    pygame.Rect(170,440,180,40), #ограда(самая самая длинная)
    pygame.Rect(500,340,120,40), # ограда (по середине побольше чем другая)
    pygame.Rect(340,545,190,40), # ограда (поменьше чем другая)
]

# КЛАСС ИГРОКА
class Player:
    def __init__(self, x, y, color, element):
        self.color = color
        self.element = element
        self.speed = 4
        self.rect = pygame.Rect(x, y, 40, 40)
    # ДВИЖЕНИЕ
    def move(self, keys):
        old_x, old_y = self.rect.x, self.rect.y
# Движение огня (WASD)
        if self.element == "fire":
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
# ДВИЖЕНИЕ ВОДЫ (Стрелки)
        if self.element == "water":
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

        # Ограничения экрана
        self.rect.x = max(0, min(WIDTH - 40, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - 40, self.rect.y))

        # Столкновение со стенами
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x, self.rect.y = old_x, old_y
                break
# РИСОВКА
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

# ОБЪЕКТЫ УРОВНЯ
lava = pygame.Rect(500, 170, 100, 20)
water = pygame.Rect(700, 575, 100, 20) 
platform = pygame.Rect(0, 580, 1200, 20)
# ВЫХОДЫ из игры
fire_exit = pygame.Rect(1140, 510, 60, 70)
water_exit = pygame.Rect(0, 105, 60, 70)

# Размещение игроков
fire = Player(100, 135, RED, "fire")
water_player = Player(1050, 540, BLUE, "water")

# ТЕКСТ
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ФУНКЦИЯ ПОЛУЧЕНИЯ ВРЕМЕНИ
def get_time():
    if final_time is not None:
        elapsed_ms = final_time
    else:
        elapsed_ms = pygame.time.get_ticks() - start_time
# Преобразование в минуты и секунды
    seconds = elapsed_ms // 1000
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02}:{seconds:02}"

# ГЛАВНЫЙ ЦИКЛ
def game():
    while True:
        clock.tick(FPS)
        screen.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Получение нажатий клавиш
        keys = pygame.key.get_pressed()

        # Движение игроков
        fire.move(keys)
        water_player.move(keys)

        # Проверка смерти игроков
        if fire.rect.colliderect(water):
            game_over("Огонь погиб в воде")
        if water_player.rect.colliderect(lava):
            game_over("Вода погибла в лаве")

        # Победа
        if fire.rect.colliderect(fire_exit) and water_player.rect.colliderect(water_exit):
            win()

        # Рисование объектов уровня
        pygame.draw.rect(screen, GRAY, platform)
        pygame.draw.rect(screen, ORANGE, lava, border_radius=6)
        pygame.draw.rect(screen, CYAN, water, border_radius=6)
        pygame.draw.rect(screen, RED, fire_exit, border_radius=6)
        pygame.draw.rect(screen, BLUE, water_exit, border_radius=6)

        # Рисуем стены
        for wall in walls:
            pygame.draw.rect(screen, GRAY, wall)

        # Рисование игроков
        fire.draw()
        water_player.draw()
        
        # Инструкции, расположение текста с лево сверху
        draw_text("Огонь — WASD", 10, 20)
        draw_text("Вода — стрелки", 1040, 20)
        draw_text(f"Время: {get_time()}", 520, 20)
        # Обновление экрана
        pygame.display.update()

# ЭКРАН Завершения игры
def game_over(text):
    ascii_art = [

    "  ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████  ",
    " ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██ ",
    " ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████  ",
    " ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██ ",
    "  ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██ ",
]
    # ШРИФТЫ
    font_ascii = pygame.font.SysFont("Courier New", 20)
    font_text = pygame.font.SysFont("arial", 26)
    # ЦИКЛ ЭКРАНА ПОРАЖЕНИЯ
    while True:
        screen.fill(BLACK)

        # ASCII арт
        start_y = 80
        for i, line in enumerate(ascii_art):
            img = font_ascii.render(line, True, WHITE)
            screen.blit(img, (WIDTH // 2 - img.get_width() // 2, start_y + i * 26))

        # Текст поражения
        text_img = font_text.render(text, True, RED)
        screen.blit(text_img, (WIDTH // 2 - text_img.get_width() // 2, 240))

        # Рестарт
        restart_img = font_text.render("Нажмите R для рестарта", True, WHITE)
        screen.blit(restart_img, (WIDTH // 2 - restart_img.get_width() // 2, 290))
        # Обработка событий выхода и рестарта
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Рестарт игры
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()
                return
        # Обновление экрана
        pygame.display.update()
        clock.tick(30)
# РЕСТАРТ ИГРЫ
def reset_game():
    global fire, water_player, start_time, final_time
# Размещение игроков
    fire.rect.x, fire.rect.y = 100, 135
    water_player.rect.x, water_player.rect.y = 1050, 540
#получение времени начала игры
    start_time = pygame.time.get_ticks() # Обновляем время начала игры
    final_time = None # Сбрасываем финальное время

# ЭКРАН ПОБЕДЫ
def win():
    global final_time

    # Фиксируем финальное время
    if final_time is None: # если еще не зафиксировано
        final_time = pygame.time.get_ticks() - start_time # время прохождения
# ЦИКЛ ЭКРАНА ПОБЕДЫ
    while True:
        clock.tick(FPS)
        screen.fill(BLUE)
# Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ТЕКСТ
        title = font.render("ПОБЕДА!", True, BLACK)
        info1 = font.render("Оба героя дошли до выхода", True, WHITE)
        info2 = font.render(f"Время прохождения: {get_time()}", True, WHITE)
        hint1 = font.render("R — перезапуск игры", True, WHITE)
        hint2 = font.render("ESC — выход", True, WHITE)

        # ОТРИСОВКА ПО ЦЕНТРУ
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180)) # от центра экрана по вертикали !строка "ПОБЕДА"
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 230)) # от центра экрана по вертикали но чуть ниже "ПОБЕДЫ" !строка "Оба героя дошли до выхода"
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 270)) # от центра экрана по вертикали но чуть ниже "Оба героя дошли до выхода" !строка "Время прохождения"
        screen.blit(hint1, (WIDTH // 2 - hint1.get_width() // 2, 340)) # от центра экрана по вертикали но чуть ниже "Время прохождения" !строка "R — перезапуск игры"
        screen.blit(hint2, (WIDTH // 2 - hint2.get_width() // 2, 380)) # от центра экрана по вертикали но чуть ниже "R — перезапуск игры" !строка "ESC — выход"

        keys = pygame.key.get_pressed()

        # ПЕРЕЗАПУСК
        if keys[pygame.K_r]:
            reset_game()
            return  # выходим из win() и продолжаем game()

        # ВЫХОД
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
# РЕСТАРТ ИГРЫ
def reset():
    fire.rect.topleft = (100, 340)
    water_player.rect.topleft = (600, 340)

# ЗАПУСК И ПЕРЕЗАПУСК ИГРЫ
reset_game()
game()
