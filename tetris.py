import pygame
import random

# Константы
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 900
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Определение фигур Тетриса
SHAPES = [
    # I
    [
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ],
        [
            [0, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ],
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    ],
    # O
    [
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1]
        ]
    ],
    # T
    [
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ]
    ],
    # L
    [
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0]
        ],
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]
    ],
    # J
    [
        [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]
        ],
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]
        ]
    ],
    # S
    [
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]
        ]
    ],
    # Z
    [
        [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
        ]
    ]
]

# Цвета фигур
COLORS = [
    (0, 255, 255),  # I - Циан
    (255, 255, 0),  # O - Желтый
    (128, 0, 128),  # T - Фиолетовый
    (255, 165, 0),  # L - Оранжевый
    (0, 0, 255),  # J - Синий
    (0, 255, 0),  # S - Зеленый
    (255, 0, 0),  # Z - Красный
]

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4 #len(self.shape)

class Tetris:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.board = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.gameover = False
        self.current_piece = Piece(GRID_WIDTH // 2, 0)
        self.next_piece = Piece(GRID_WIDTH // 2, 0)

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Piece(GRID_WIDTH // 2, 0)
        if self.check_collision(self.current_piece):
            self.gameover = True

    def check_collision(self, piece):
        image = piece.image()
    #    print("Image: ", image)  # Отладочный вывод
        if not isinstance(image, list) or not all(isinstance(row, list) for row in image):
            raise ValueError("The image must be a list of lists")

        for y, row in enumerate(piece.image()):
            for x, cell in enumerate(row):
                if cell and (
                        x + piece.x < 0 or
                        x + piece.x >= GRID_WIDTH or
                        y + piece.y >= GRID_HEIGHT or
                        self.board[y + piece.y][x + piece.x] != (0, 0, 0)
                ):
                    return True
        return False

    def freeze(self):
        for y, row in enumerate(self.current_piece.image()):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_piece.y][x + self.current_piece.x] = self.current_piece.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        lines = 0
        for y in range(GRID_HEIGHT):
            if (0, 0, 0) not in self.board[y]:
                lines += 1
                del self.board[y]
                self.board.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])
        self.score += lines ** 2

    def move(self, dx):
        self.current_piece.x += dx
        if self.check_collision(self.current_piece):
            self.current_piece.x -= dx

    def drop(self):
        self.current_piece.y += 1
        if self.check_collision(self.current_piece):
            self.current_piece.y -= 1
            self.freeze()

    def rotate(self):
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.rotate()
            self.current_piece.rotate()
            self.current_piece.rotate()

    def draw_grid(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, self.board[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def draw_piece(self, screen, piece):
        for y, row in enumerate(piece.image()):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, piece.color, ((piece.x + x) * GRID_SIZE, (piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()
        # Шрифт для отображения текста
        font = pygame.font.SysFont(None, 36)

        while not self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1)
                    elif event.key == pygame.K_DOWN:
                        self.drop()
                    elif event.key == pygame.K_UP:
                        self.rotate()

            self.drop()
            screen.fill((0, 0, 0))
            self.draw_grid(screen)
            self.draw_piece(screen, self.current_piece)

            text = font.render(f"Полных строк: {self.score} ", True, (255, 255, 255))
            screen.blit(text, (10, 10))

            pygame.display.flip()
       #     clock.tick(10 + self.level)
            clock.tick(5 + self.level)

        pygame.quit()

if __name__ == "__main__":

    game = Tetris()
    game.run()
