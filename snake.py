import pygame
import random
from pygame.locals import *

# Settings
SIZE = 15
BOARD_WIDTH = 25
BOARD_HEIGHT = 20
SCREEN_WIDTH = BOARD_WIDTH * SIZE
SCREEN_HEIGHT = BOARD_HEIGHT * SIZE

UP = (0, -SIZE)
LEFT = (-SIZE, 0)
DOWN = (0, SIZE)
RIGHT = (SIZE, 0)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()

font_xl = pygame.font.Font("./font.ttf", 16, bold=pygame.font.Font.bold)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [(x, y)]
        self.direction = RIGHT
        self.length = 5

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

        if (self.x < 0):
            self.x = SCREEN_WIDTH - SIZE
        if (self.x >= SCREEN_WIDTH):
            self.x = 0
        if (self.y < 0):
            self.y = SCREEN_HEIGHT - SIZE
        if (self.y >= SCREEN_HEIGHT):
            self.y = 0

        self.body.append((self.x, self.y))
        if (len(self.body) > self.length):
            del self.body[0]

    def change_direction(self, direction):
        if ((self.direction == DOWN and direction == UP) or
            (self.direction == UP and direction == DOWN) or
            (self.direction == RIGHT and direction == LEFT) or
                (self.direction == LEFT and direction == RIGHT)):
            return
        self.direction = direction

    def collide_with_food(self, food):
        return (self.x, self.y) == (food.x, food.y)

    def append(self):
        self.length += 1

    def check_game_over(self):
        return (self.x, self.y) in self.body[0: -1]

    def render(self):
        for pos in self.body:
            pygame.draw.rect(screen, WHITE, (pos[0], pos[1], SIZE, SIZE))

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update_position(self, snake):
        while True:
            x = random.randint(0, BOARD_WIDTH - 1) * SIZE
            y = random.randint(0, BOARD_HEIGHT - 1) * SIZE
            if (not ([x, y] in snake.body)):
                break
        self.x = x
        self.y = y

    def render(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, SIZE, SIZE))

class GameScene:
    def __init__(self):
        self.snake = Snake(BOARD_WIDTH // 2 * SIZE, BOARD_HEIGHT // 2 * SIZE)
        self.food = Food()
        self.food.update_position(self.snake)
        self.next_scene = self

    def process_input(self, event):
        if event.key == pygame.K_w:
            self.snake.change_direction(UP)
        elif event.key == pygame.K_a:
            self.snake.change_direction(LEFT)
        elif event.key == pygame.K_s:
            self.snake.change_direction(DOWN)
        elif event.key == pygame.K_d:
            self.snake.change_direction(RIGHT)

    def update(self):
        self.snake.move()

        if (self.snake.collide_with_food(self.food)):
            self.snake.append()
            self.food.update_position(self.snake)

        if (self.snake.check_game_over()):
            self.next_scene = TitleScene("- - - GAME OVER - - -")

    def render(self):
        screen.fill(BLACK)
        self.snake.render()
        self.food.render()

class TitleScene:
    def __init__(self, title):
        self.title = title
        self.next_scene = self

    def process_input(self, event):
        self.next_scene = GameScene()

    def update(self): pass

    def render(self):
        text = font_xl.render(self.title, 1, WHITE)
        rect = text.get_rect()
        rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, rect)

class Main:
    def __init__(self):
        self.scene = TitleScene("- - - Press any key to start - - -")

    def run(self):
        run = True
        while run:
            # Manage user input
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    self.scene.process_input(event)

            # Manage scene
            self.scene.update()
            self.scene.render()
            self.scene = self.scene.next_scene

            # Update and tick
            pygame.display.update()
            clock.tick(15)

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
