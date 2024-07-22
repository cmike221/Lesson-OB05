import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# Определение цветов
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создание окна игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

# Класс для еды
class Food:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def relocate(self):
        self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE

# Класс для змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [self.random_position()]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = GREEN

    def random_position(self):
        return (random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
                random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (self.length > 1 and
                (point[0] * -1, point[1] * -1) == self.direction):
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * BLOCK_SIZE)) % SCREEN_WIDTH),
               (cur[1] + (y * BLOCK_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [self.random_position()]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def draw(self, screen):
        for p in self.positions:
            pygame.draw.rect(screen, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.turn((0, -1))
                elif event.key == pygame.K_s:
                    self.turn((0, 1))
                elif event.key == pygame.K_a:
                    self.turn((-1, 0))
                elif event.key == pygame.K_d:
                    self.turn((1, 0))

# Основная функция игры
def game():
    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()

    while True:
        snake.handle_keys()
        snake.move()
        if snake.get_head_position() == (food.x, food.y):
            snake.length += 1
            food.relocate()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()

        if snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= SCREEN_WIDTH or \
           snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= SCREEN_HEIGHT:
            snake.reset()

        clock.tick(10)

if __name__ == "__main__":
    game()
