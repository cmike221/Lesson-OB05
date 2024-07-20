import pygame
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 10
NUM_BRICKS = 8

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Арканоид")

# Класс для платформы
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            SCREEN_HEIGHT - PADDLE_HEIGHT - 10,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        self.speed = 10

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

# Класс для шара
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - BALL_SIZE) // 2,
            SCREEN_HEIGHT // 2,
            BALL_SIZE,
            BALL_SIZE
        )
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, (0, 255, 0), self.rect)

    def reset(self):
        self.rect.x = (SCREEN_WIDTH - BALL_SIZE) // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

# Класс для кирпичей
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

# Создание объектов
paddle = Paddle()
ball = Ball()
bricks = [Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 35) for x in range(NUM_BRICKS) for y in range(3)]

# Игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    ball.move()

    # Проверка столкновений шара с платформой
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y *= -1

    # Проверка столкновений шара с кирпичами
    for brick in bricks:
        if brick.alive and ball.rect.colliderect(brick.rect):
            ball.speed_y *= -1
            brick.alive = False

    # Проверка падения шара
    if ball.rect.bottom >= SCREEN_HEIGHT:
        ball.reset()

    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
