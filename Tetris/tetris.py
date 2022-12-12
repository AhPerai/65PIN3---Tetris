import pygame, random
import screen_utils as Screen
from Tetris.shapes import *
from Tetris.constants import *
from Utils.commands import *
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
    lines_cleared: int
    grid: List[List[Tuple[int, int, int]]]
    info : list
    shape_list : list
    
    def __init__(self, info, shape_list = None):
        pygame.font.init() 
        # Auxiliares para a Simulação
        self.info = info
        self.shape_list = shape_list
        self.shape_counter = 0
        #Variaveis para o game
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.blocked_pos = dict()
        self.game_running = True
        self.game_over = False
        self.next_piece = self.get_shape()
        self.current_piece = self.get_shape()
        self.change_current_piece = False
        self.shape_pos = list()
        self.game_clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 0.27
        self.lines_cleared = 0
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
    
    def get_shape(self):
        if self.shape_list is None:
            return Piece(5, 0,random.choice(shapes))
        
        piece = Piece(5,0, self.shape_list[self.shape_counter])
        self.shape_counter +=1
        if self.shape_counter > len(self.shape_list)-1: self.shape_counter = 0
        return piece

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
        return inc
        
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
        font = pygame.font.SysFont('poppins', 60)
        label = font.render('TETRIS', 1, (255,255,255)) 
        
        self.window.blit(label, (TOP_LEFT_X_AXIS + GRID_WIDTH / 2 - (label.get_width()/2), 30))
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(self.window, self.grid[i][j], (TOP_LEFT_X_AXIS + j*BLOCK_SIZE, TOP_LEFT_y_AXIS+ i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                
        pygame.draw.rect(self.window, (255,0,0), (TOP_LEFT_X_AXIS, TOP_LEFT_y_AXIS, GRID_WIDTH, GRID_HEIGHT), 5)
        
        # self.draw_grid()
        
        font = pygame.font.SysFont('poppins', 30)
        lblScore = font.render(f'SCORE: {self.score}', 1, (255,255,255))
        lblLines = font.render(f'LINES: {self.lines_cleared}' , 1, (255,255,255))
        sx = TOP_LEFT_X_AXIS + GRID_WIDTH + 50
        sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
        self.window.blit(lblScore, (sx, sy + 160))
        self.window.blit(lblLines, (sx, sy + 190))
                    
    def draw_model_info(self, info):
        generation = info[0]
        run = info[1]
        model = info[2]
        font = pygame.font.SysFont('poppins', 30)
        components = []
        components.append(font.render(f'GENERATION: {generation}',     1, (255,255,255)))
        components.append(font.render('MODEL', 1, (255,255,255)))
        components.append(font.render(f'id: {model.id}',     1, (255,255,255)))
        components.append(font.render(f'run: {run}',     1, (255,255,255)))
        components.append(font.render(f'Height: {round(model.weights[0], 2)}',     1, (255,255,255)))
        components.append(font.render(f'Holes: {round(model.weights[1], 2)}',     1, (255,255,255)))
        components.append(font.render(f'Bumpiness:{round(model.weights[2], 2)}', 1, (255,255,255)))
        components.append(font.render(f'Pits: {round(model.weights[3], 2)}',     1, (255,255,255)))
        components.append(font.render(f'Clear lines: {round(model.weights[4], 2)}',    1, (255,255,255)))
    
        sx = TOP_LEFT_X_AXIS + GRID_WIDTH - 500
        sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
        pos_y = 60
        for label in components:
            pos_y -= 30  
            self.window.blit(label, (sx + 10, sy - pos_y))     
                        
                    
    def main(self, action=None):
        self.create_grid()
                   
        self.fall_time += self.game_clock.get_rawtime()
        self.game_clock.tick()
        
        if self.fall_time/1000 >= self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not (self.current_piece.isInValidSpace(self.grid)) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_current_piece = True 
        
        if action is not None:
            if action == DO_ROTATE: doRotate(self.current_piece, self.grid)
            elif action == GO_LEFT: goLeft(self.current_piece, self.grid)
            elif action == GO_RIGHT: goRight(self.current_piece, self.grid)
            elif action == GO_DOWN: goDown(self.current_piece, self.grid)
            elif action == PRESS_DOWN:
                while self.current_piece.isInValidSpace(self.grid): 
                    self.current_piece.y += 1
                self.current_piece.y -= 1
                self.change_current_piece = True
    
        self.shape_pos = self.current_piece.getFormatedShape()
    
        for i in range(len(self.shape_pos)):
            x, y = self.shape_pos[i]
            if y > -1:
                self.grid[y][x]= self.current_piece.color
                
        
        #atualizando posicoes bloqueadas
        if self.change_current_piece:
            for pos in self.shape_pos:
                p = (pos[0], pos[1])
                self.blocked_pos[p] = self.current_piece.color
                                
            #Atualização da tela 
            self.create_grid()
            #Criação do próximo formato 
            self.current_piece = self.next_piece
            self.next_piece = self.get_shape()
            self.change_current_piece = False
            self.lines_cleared += self.clear_rows()
            self.score +=  5     
                           
        self.draw_window()
        self.draw_next_shape()
        self.draw_model_info(self.info)
        pygame.display.update() 
            
        if self.check_lost():
            self.change_current_piece = False
            self.game_over = True  
            Screen.draw_text_middle(self.window, "Jogo Finalizado", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(100) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.display.quit() 
            
            
            
                     


