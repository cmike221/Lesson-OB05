import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Размеры ракеток и мяча
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20

# Скорость игры
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Классы
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def bounce(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

# Создание объектов
player_paddle = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.rect.top > 0:
        player_paddle.move(up=True)
    if keys[pygame.K_DOWN] and player_paddle.rect.bottom < HEIGHT:
        player_paddle.move(up=False)

    # Управление соперником (AI)
    if opponent_paddle.rect.centery < ball.rect.centery and opponent_paddle.rect.bottom < HEIGHT:
        opponent_paddle.move(up=False)
    if opponent_paddle.rect.centery > ball.rect.centery and opponent_paddle.rect.top > 0:
        opponent_paddle.move(up=True)

    # Движение мяча
    ball.move()
    ball.bounce()

    # Проверка коллизий мяча с ракетками
    if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
        ball.speed_x = -ball.speed_x

    # Отрисовка объектов
    screen.fill(BLACK)
    player_paddle.draw()
    opponent_paddle.draw()
    ball.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
