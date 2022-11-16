import pygame, random
import screen_utils as Screen
from Tetris.shapes import *
from Tetris.constants import *
from Tetris.commands import *
from Tetris.piece import Piece
from typing import List, Tuple, Dict

pygame.font.init()

class Tetris: 
    window: pygame.Surface
    fall_speed: float
    fall_time: int
    game_clock: pygame.time.Clock
    change_current_piece: bool
    next_piece: Piece
    current_piece: Piece
    game_over: bool
    game_running: bool
    blocked_pos: Dict[Tuple[int, int], Tuple[int, int, int]]
    score: int
    grid: List[List[Tuple[int, int, int]]]
    
    def __init__(self): 
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]
        self.score = -5
        self.blocked_pos = dict()
        self.game_running = True
        self.game_over = False
        self.next_piece = Piece(5, 0,random.choice(shapes))
        self.current_piece = self.next_piece
        self.change_current_piece = True
        self.shape_pos = list()
        self.game_clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 0.27
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def get_shape(self):
        return Piece(5, 0,random.choice(shapes))

    def create_grid(self):
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in self.blocked_pos:
                    self.grid[i][j] = self.blocked_pos[(j,i)]
                else: 
                    self.grid[i][j] = (0,0,0)
                    
        return self.grid     

    def check_lost(self):
        for pos in self.blocked_pos:
            x, y = pos
            if y < 1:
                return True
        return False
                
    def clear_rows(self):
        inc = 0
        for i in range(len(self.grid)):
            if (0, 0, 0) not in self.grid[i]:
                inc += 1
                for j in range(len(self.grid[i])):
                    if (j, i) in self.blocked_pos.keys():
                        del self.blocked_pos[(j, i)]
                
                updated_blocked_positions = dict()
                
                for pos, val in self.blocked_pos.items():
                    x, y = pos
                    if y < i:
                        updated_blocked_positions[(x, y+1)] = val
                    else: 
                        updated_blocked_positions[(x, y)] = val 
                        
                self.blocked_pos = updated_blocked_positions
        
        self.score += SCORE_BY_LINE_CLEARED[inc]
        

    def draw_grid(self):
        x = TOP_LEFT_X_AXIS
        y = TOP_LEFT_y_AXIS
        
        for i in range(len(self.grid)):
            pygame.draw.line(self.window, (128,128,128), (x, y + i*BLOCK_SIZE), (x + GRID_WIDTH, y+ i*BLOCK_SIZE))
            for i in range(len(self.grid[i])):
                pygame.draw.line(self.window, (128,128,128), (x + i*BLOCK_SIZE, y), (x + i*BLOCK_SIZE, y + GRID_HEIGHT))

    def draw_next_shape(self):
        font = pygame.font.SysFont('poppins', 30)
        label = font.render('Próximo bloco:', 1, (255,255,255))

        sx = TOP_LEFT_X_AXIS + GRID_WIDTH + 50
        sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
        format = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.window, self.next_piece.color, (sx + j*30, sy + i*30, 30, 30), 0)

        self.window.blit(label, (sx + 10, sy- 30))

    def draw_window(self):
        self.window.fill(( 0, 0, 0))   
        pygame.font.init()
        font = pygame.font.SysFont('poppins', 60)
        label = font.render('Tetris', 1, (255,255,255)) 
        
        self.window.blit(label, (TOP_LEFT_X_AXIS + GRID_WIDTH / 2 - (label.get_width()/2), 30))
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                #pygame.draw.rect(supericie, cor, posX, posY, width, height, fill)
                pygame.draw.rect(self.window, self.grid[i][j], (TOP_LEFT_X_AXIS + j*BLOCK_SIZE, TOP_LEFT_y_AXIS+ i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                
        pygame.draw.rect(self.window, (255,0,0), (TOP_LEFT_X_AXIS, TOP_LEFT_y_AXIS, GRID_WIDTH, GRID_HEIGHT), 5)
        
        self.draw_grid()
        
        font = pygame.font.SysFont('poppins', 30)
        label = font.render('SCORE: '+ str(self.score), 1, (255,255,255))

        sx = TOP_LEFT_X_AXIS + GRID_WIDTH + 50
        sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
        self.window.blit(label, (sx + 25, sy + 160))

                    
    def main(self, action=None):
        self.create_grid()
            
        #atualizando posicoes bloqueadas
        if self.change_current_piece:
            for pos in self.shape_pos:
                if __debug__:
                    if pos[0] == -1 or pos[1] == -1:
                        print(str(pos[0]), str(pos[1]))
                p = (pos[0], pos[1])
                self.blocked_pos[p] = self.current_piece.color
                self.create_grid()
                
            #Criação do próximo formato 
            self.current_piece = self.next_piece
            self.next_piece = self.get_shape()
            self.change_current_piece = False
            self.clear_rows()
            self.score +=  5            
    
        self.fall_time += self.game_clock.get_rawtime()
        self.game_clock.tick()
        
        if self.fall_time/1000 >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not (self.current_piece.isInValidSpace(self.grid)) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_current_piece = True 
        
        if action is not None:
            if action == PRESS_ROTATE: doRotate(self.current_piece, self.grid)
            if action == PRESS_LEFT: goLeft(self.current_piece, self.grid)
            if action == PRESS_RIGHT: goRight(self.current_piece, self.grid)
            if action == PRESS_DOWN: 
                goDown(self.current_piece, self.grid)
    
        self.shape_pos = self.current_piece.getFormatedShape()
    
        for i in range(len(self.shape_pos)):
            x, y = self.shape_pos[i]
            if y > -1:
                self.grid[y][x]= self.current_piece.color
                    
        self.draw_window()
        self.draw_next_shape()
        pygame.display.update() 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.display.quit() 
            
        if self.check_lost():
            self.change_current_piece = False
            self.game_over = True  
            Screen.draw_text_middle(self.window, "Jogo Finalizado", 80, (255, 255, 255))
            pygame.display.update()
            print(self.blocked_pos)
            pygame.time.delay(100) 
            
            
            
                     


