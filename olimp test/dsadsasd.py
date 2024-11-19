import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Семейный квест")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Персонаж игрока
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_color = BLUE

# Члены семьи
family = [
    {"name": "Мама", "pos": [150, 150], "color": GREEN, "task": "Приготовь ужин", "completed": False, "type": "cooking"},
    {"name": "Папа", "pos": [650, 150], "color": GREEN, "task": "Убери в комнате", "completed": False, "type": "cleaning"},
    {"name": "Брат", "pos": [150, 450], "color": GREEN, "task": "Сделай домашку", "completed": False, "type": "quiz"},
    {"name": "Сестра", "pos": [650, 450], "color": GREEN, "task": "Поиграй с собакой", "completed": False, "type": "dodge"},
]

# Шрифт
font = pygame.font.Font(None, 36)

# Счет
score = 0
clock = pygame.time.Clock()

# Название квеста
quest_title = "Семейный квест: Помоги семье!"

# Функция отображения текста
def draw_text(text, x, y, color=BLACK, font_size=36):
    font = pygame.font.Font(None, font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))


# Мини-игра: Приготовить ужин (нажмите кнопки в порядке)
def cooking_game():
    screen.fill(WHITE)
    draw_text("Мини-игра: Приготовь ужин", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, font_size=48)
    pygame.display.flip()
    pygame.time.wait(1000)

    correct_sequence = ["A", "B", "C"]
    input_sequence = []

    draw_text("Нажмите A, B, C по порядку", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20)
    pygame.display.flip()
    while len(input_sequence) < len(correct_sequence):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() in correct_sequence:
                    input_sequence.append(event.unicode.upper())
    return input_sequence == correct_sequence


# Мини-игра: Уборка комнаты (соберите мусор)
def cleaning_game():
    screen.fill(WHITE)
    draw_text("Мини-игра: Убери в комнате", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, font_size=48)
    pygame.display.flip()
    pygame.time.wait(1000)

    player_x, player_y = player_pos
    items = [{"x": random.randint(50, SCREEN_WIDTH - 50), "y": random.randint(50, SCREEN_HEIGHT - 50)} for _ in range(5)]
    collected_items = 0
    duration = 20000  # Игра длится 20 секунд
    start_time = pygame.time.get_ticks()

    while collected_items < len(items) and pygame.time.get_ticks() - start_time < duration:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
            player_x += 5
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_size:
            player_y += 5

        # Отрисовка игрока
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Отрисовка предметов
        for item in items:
            if item:  # Если предмет еще не собран
                pygame.draw.circle(screen, GREEN, (item["x"], item["y"]), 15)

        # Проверка на сбор предметов
        for i, item in enumerate(items):
            if item and pygame.Rect(player_x, player_y, player_size, player_size).colliderect(
                pygame.Rect(item["x"] - 15, item["y"] - 15, 30, 30)
            ):
                items[i] = None  # Убираем собранный предмет
                collected_items += 1

        # Отображение прогресса и таймера
        draw_text(f"Собрано: {collected_items}/{len(items)}", 10, 10)
        remaining_time = (duration - (pygame.time.get_ticks() - start_time)) // 1000
        draw_text(f"Время: {remaining_time}s", 10, 40)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(30)

    # Проверка на победу или поражение
    if collected_items == len(items):
        draw_text("Вы собрали всё!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, GREEN)
    else:
        draw_text("Время вышло!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, RED)
    
    pygame.display.flip()
    pygame.time.wait(3000)

    return collected_items == len(items)  # True, если победа


# Мини-игра: Домашка (вопрос с вводом)
def quiz_game():
    screen.fill(WHITE)
    draw_text("Мини-игра: Сделай домашку", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, font_size=48)
    pygame.display.flip()
    pygame.time.wait(1000)

    question = "Сколько будет 5 + 3?"
    answer = "8"
    user_input = ""
    while True:
        screen.fill(WHITE)
        draw_text(question, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        draw_text(f"Ваш ответ: {user_input}", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    user_input += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    return user_input == answer


# Мини-игра: Уклонение от предметов
def dodge_game():
    screen.fill(WHITE)
    draw_text("Мини-игра: Поиграй с собакой", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, font_size=48)
    pygame.display.flip()
    pygame.time.wait(1000)

    player_x, player_y = player_pos
    obstacles = [{"x": random.randint(0, SCREEN_WIDTH - 30), "y": 0, "speed": random.randint(2, 5)} for _ in range(5)]
    start_time = pygame.time.get_ticks()
    duration = 15000  # Игра длится 15 секунд

    while pygame.time.get_ticks() - start_time < duration:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
            player_x += 5
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_size:
            player_y += 5

        # Отрисовка игрока
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Отрисовка и движение препятствий
        for obstacle in obstacles:
            obstacle["y"] += obstacle["speed"]
            if obstacle["y"] > SCREEN_HEIGHT:
                obstacle["y"] = 0
                obstacle["x"] = random.randint(0, SCREEN_WIDTH - 30)

            pygame.draw.rect(screen, RED, (obstacle["x"], obstacle["y"], 30, 30))

            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(pygame.Rect(obstacle["x"], obstacle["y"], 30, 30)):
                return False  # Игрок проиграл, если столкнулся с препятствием

        pygame.display.flip()
        clock.tick(30)

    return True  # Победа

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)

    # Отображение названия квеста
    draw_text(quest_title, SCREEN_WIDTH // 2 - 150, 10, color=BLACK, font_size=48)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += 5
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += 5

    # Отрисовка игрока
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    # Отрисовка членов семьи
    for member in family:
        color = RED if member["completed"] else member["color"]
        pygame.draw.circle(screen, color, member["pos"], 30)
        draw_text(member["name"], member["pos"][0] - 25, member["pos"][1] - 40)

    # Проверка на столкновение
    for member in family:
        if not member["completed"]:
            member_rect = pygame.Rect(member["pos"][0] - 30, member["pos"][1] - 30, 60, 60)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
            if player_rect.colliderect(member_rect):
                if member["type"] == "cooking" and cooking_game():
                    member["completed"] = True
                elif member["type"] == "cleaning" and cleaning_game():
                    member["completed"] = True
                elif member["type"] == "quiz" and quiz_game():
                    member["completed"] = True
                elif member["type"] == "dodge" and dodge_game():
                    member["completed"] = True
                if member["completed"]:
                    score += 1

    # Отображение текущего задания и счета
    draw_text(f"Счет: {score}", 10, 10)

    # Победа
    if all(member["completed"] for member in family):
        draw_text("Вы выиграли!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
