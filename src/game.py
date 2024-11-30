import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()  
font = pygame.font.SysFont('arial', 25)  

# Representa as direções que a cobra pode tomar (direita, esquerda, cima, baixo)
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')  
BLOCK_SIZE = 20  
SPEED = 50  

# Cores RGB utilizadas
BROWN = (130,87,61)
BLACK = (0,0,0)
GREEN1 = (0,180,0)
GREEN2 = (0,235,0)
GRAY1 = (80,80,80)
GRAY2 = (90,90,90)
DARK_BROWN = (113,76,54)
RED1 = (200,0,0)
RED2 = (255,0,0)
WHITE = (255,255,255)

class SnakeGameAI:
    # Especificações do Jogo
    def __init__(self, w=680, h=520):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))  
        pygame.display.set_caption('SnakeGAME')  
        self.clock = pygame.time.Clock()  
        self.reset()

    # Estado inicial do jogo
    def reset(self):
        self.direction = Direction.RIGHT  
        self.head = Point(self.w / 2, self.h / 2)  
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y)]  
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    # Movimenta��o da cobra
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]  
        idx = clock_wise.index(self.direction)  

        if np.array_equal(action, [1, 0, 0]):  
            new_dir = clock_wise[idx]  
        elif np.array_equal(action, [0, 1, 0]):  
            next_idx = (idx + 1) % 4 
            new_dir = clock_wise[next_idx]  
        else:  
            next_idx = (idx - 1) % 4  
            new_dir = clock_wise[next_idx]  

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)  
    
    # Gerador de comida
    def _place_food(self):
        x = random.randint(2, (self.w - BLOCK_SIZE*3) // BLOCK_SIZE ) * BLOCK_SIZE  
        y = random.randint(2, (self.h - BLOCK_SIZE*3) // BLOCK_SIZE ) * BLOCK_SIZE  
        self.food = Point(x, y)  
        if self.food in self.snake:  
            self._place_food()  

    # Gerador do tabuleiro
    def _draw_Board(self):
        for i in range(self.w):
            # Cima
            pygame.draw.rect(self.display, GRAY1, pygame.Rect(i*40, 0, BLOCK_SIZE*2, BLOCK_SIZE*2))
            pygame.draw.rect(self.display, GRAY2, pygame.Rect(i*40 + 6.5, 0 + 6.5, BLOCK_SIZE+8, BLOCK_SIZE+8))
            # Baixo
            pygame.draw.rect(self.display, GRAY1, pygame.Rect(i*40, self.h-40, BLOCK_SIZE*2, BLOCK_SIZE*2))
            pygame.draw.rect(self.display, GRAY2, pygame.Rect(i*40 + 6.5, self.h-40 + 6.5, BLOCK_SIZE+8, BLOCK_SIZE+8))
            # Direita
            pygame.draw.rect(self.display, GRAY1, pygame.Rect(self.w-40, i*40, BLOCK_SIZE*2, BLOCK_SIZE*2))
            pygame.draw.rect(self.display, GRAY2, pygame.Rect(self.w-40 + 6.5, i*40 + 6.5, BLOCK_SIZE+8, BLOCK_SIZE+8))
            # Esquerda
            pygame.draw.rect(self.display, GRAY1, pygame.Rect(0, i*40, BLOCK_SIZE*2, BLOCK_SIZE*2))
            pygame.draw.rect(self.display, GRAY2, pygame.Rect(0 + 6.5, i*40 + 6.5, BLOCK_SIZE+8, BLOCK_SIZE+8))
    
    # Gerador de linhas na tela
    def _draw_Grid(self):
        blocks_x = self.w // BLOCK_SIZE
        blocks_y = self.h // BLOCK_SIZE
        
        # Desenhar linhas verticais
        for col in range(1, blocks_x):  
            x = col * BLOCK_SIZE
            pygame.draw.line(self.display, DARK_BROWN, (x, 0), (x, self.h))
        # Desenhar linhas horizontais
        for row in range(1, blocks_y): 
            y = row * BLOCK_SIZE
            pygame.draw.line(self.display, DARK_BROWN, (0, y), (self.w, y))

    # Define posição dos olhos da cobra
    def _eyes(self):
        centre = BLOCK_SIZE // 2
        radius = 3
        if self.direction == Direction.RIGHT:
            eye1 = (self.head.x + BLOCK_SIZE - radius*2, self.head.y + centre  - radius -1)
            eye2 = (self.head.x + BLOCK_SIZE - radius*2, self.head.y + BLOCK_SIZE - radius*2)
        elif self.direction == Direction.LEFT:
            eye1 = (self.head.x + centre - radius, self.head.y + centre  - radius - 1)
            eye2 = (self.head.x + centre - radius, self.head.y + BLOCK_SIZE - radius*2)
        elif self.direction == Direction.UP:
            eye1 = (self.head.x + centre - radius - 1, self.head.y + centre  - radius)
            eye2 = (self.head.x + BLOCK_SIZE - radius*2, self.head.y + centre  - radius)
        elif self.direction == Direction.DOWN:
            eye1 = (self.head.x + centre - radius - 1, self.head.y + BLOCK_SIZE - radius*2)
            eye2 = (self.head.x + BLOCK_SIZE - radius*2, self.head.y + BLOCK_SIZE - radius*2)
        pygame.draw.circle(self.display, BLACK, eye1, radius)  
        pygame.draw.circle(self.display, BLACK, eye2, radius)

    # Atualização da Interface do Usuário
    def _update_ui(self):
        self.display.fill(BROWN) 
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))  

        self._eyes()
        pygame.draw.rect(self.display, RED1, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))  
        pygame.draw.rect(self.display, RED2, pygame.Rect(self.food.x + 4, self.food.y + 4, 12, 12))  
        self._draw_Grid()
        self._draw_Board()

        text = font.render("Score: " + str(self.score), True, WHITE)  
        self.display.blit(text, [10, 5]) 
        pygame.display.flip()  

    # Verificador de colisões
    def is_collision(self, pt=None):
        if pt is None:  
            pt = self.head  
        if pt.x > self.w - BLOCK_SIZE*3 or pt.x < 40 or pt.y > self.h - BLOCK_SIZE*3 or pt.y < 40: 
            return True
        if pt in self.snake[1:]:
            return True
        return False

    # Executador de ações
    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()

        self._move(action) 
        self.snake.insert(0, self.head)  #
        
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 250 * len(self.snake):  
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:  
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()  
        
        self._update_ui()
        self.clock.tick(SPEED)  
        return reward, game_over, self.score
