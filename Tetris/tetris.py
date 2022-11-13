import pygame, random, numpy as np
from Tetris.shapes import *

pygame.font.init()

#VARIAVEIS GLOBAIS
screen_width = 800
screen_height = 700
block_size = 30
play_height = block_size * 20
play_width =  block_size * 10

#Auxiliares para lidar com a posicionamento
top_left_x = (screen_width - play_width) / 2
top_left_y = screen_height - play_height

#FORMATO DOS BLOCOS 

# S = [['.....',
#       '......',
#       '..00..',
#       '.00...',
#       '.....'],
#      ['.....',
#       '..0..',
#       '..00.',
#       '...0.',
#       '.....'],
#      ['.....',
#       '.....',
#       '.00..',
#       '..00.',
#       '.....'],
#      ['.....',
#       '..0..',
#       '.00..',
#       '.0...',
#       '.....']]

# I = [['..0..',
#       '..0..',
#       '..0..',
#       '..0..',
#       '.....'],
#      ['.....',
#       '0000.',
#       '.....',
#       '.....',
#       '.....']]

# O = [['.....',
#       '.....',
#       '.00..',
#       '.00..',
#       '.....']]

# J = [['.....',
#       '.0...',
#       '.000.',
#       '.....',
#       '.....'],
#      ['.....',
#       '..00.',
#       '..0..',
#       '..0..',
#       '.....'],
#      ['.....',
#       '.....',
#       '.000.',
#       '...0.',
#       '.....'],
#      ['.....',
#       '..0..',
#       '..0..',
#       '.00..',
#       '.....']]

# L = [['.....',
#       '...0.',
#       '.000.',
#       '.....',
#       '.....'],
#      ['.....',
#       '..0..',
#       '..0..',
#       '..00.',
#       '.....'],
#      ['.....',
#       '.....',
#       '.000.',
#       '.0...',
#       '.....'],
#      ['.....',
#       '.00..',
#       '..0..',
#       '..0..',
#       '.....']]

# T = [['.....',
#       '..0..',
#       '.000.',
#       '.....',
#       '.....'],
#      ['.....',
#       '..0..',
#       '..00.',
#       '..0..',
#       '.....'],
#      ['.....',
#       '.....',
#       '.000.',
#       '..0..',
#       '.....'],
#      ['.....',
#       '..0..',
#       '.00..',
#       '..0..',
#       '.....']]

# shapes = [S, I, O, J, L, T]  
# shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]; 
        self.rotation = 0

def create_grid(locked_blocks={}):
    grid = [[(0,0,0) for i in range(10)] for i in range(20)]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_blocks:
                b = locked_blocks[(j,i)]
                grid[i][j] = b
                
    return grid
        
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    
    formatted = convert_shape_format(shape)
    
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0,random.choice(shapes))

def draw_text_middle(surface, text, size, color):  
    font = pygame.font.SysFont("poppins", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
    x = top_left_x
    y = top_left_y
    
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (x, y + i*block_size), (x + play_width, y+ i*block_size))
        for i in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (x + i*block_size, y), (x + i*block_size, y + play_height))
            
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('poppins', 30)
    label = font.render('Próximo bloco:', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))

def draw_window(surface, grid, score =0):
    surface.fill(( 0, 0, 0))   
    pygame.font.init()
    font = pygame.font.SysFont('poppins', 60)
    label = font.render('Tetris', 1, (255,255,255)) 
    
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()/2), 30))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #pygame.draw.rect(supericie, cor, posX, posY, width, height, fill)
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y+ i*block_size, block_size, block_size), 0)
            
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)
    
    draw_grid(surface, grid)
    
    font = pygame.font.SysFont('poppins', 30)
    label = font.render('Pontuação: ', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 25, sy + 160))
    
def mapPossibleMoves(grid, blocked_position, shape):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    highest_blocks = {0: 20, 1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
    for pos in blocked_position:
        i, j = pos
        if j < highest_blocks.get(i): highest_blocks[i] = j
    
    rotations = getRotationPosition(shape)
    
    for i in rotations: 
        getValidMoves(highest_blocks, accepted_pos, rotations.get(i), i)
    
    print('calculado')
    
def getRotationPosition(shape): 
    rotations = {}
    for rotation in range(len(shape.shape)): 
        format = shape.shape[rotation % len(shape.shape)]
        positions = []
        left_point = 4
        right_point = 0
        lowest_column = 0     
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((j,i)) 
                    lowest_column = j
                    if j < left_point: left_point = j
                    if j > right_point: right_point = j  

        lenght = 1+(right_point - left_point) 
        
        lowest_column -= left_point
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - left_point, pos[1]) 
            
        rotations[rotation] = positions, lenght, lowest_column 
         
    return rotations

def getValidMoves(highest_blocks, accepted_pos, shape, rotation):
    validMoves = []
    
    for i in range(10):
        highest_block = highest_blocks.get(i)
        j = i
        highest_col = shape[2] + i
        for j in range(shape[1] + i):
            if j > 9: break
            if highest_blocks.get(j) < highest_block:
                highest_block = highest_blocks.get(j)
                highest_col = j 
                
        base_row = 0
        for pos in shape[0]: 
            if pos[0] == highest_col and pos[1] > base_row: base_row = pos[1]
            
        for pos in shape[0]:
            col = pos[0]+i
            row = pos[1]+highest_block-1-base_row
            pos = col, row
            if pos not in accepted_pos: continue
        
        play = rotation, i
        validMoves.append(play)
    
    return validMoves
                  
def main(windown):
    
    blocked_position = {}
    grid = create_grid(blocked_position)
    shape_pos = []
    next_piece = get_shape()
    
    change_piece = True
    run = True
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0
    
    while run:
        #atualizando posicoes bloqueadas
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                blocked_position[p] = current_piece.color
                
            #Criação do próximo formato 
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, blocked_position) * 10
            # mapPossibleMoves(grid, blocked_position, current_piece)
        
        fall_speed = 0.27
        
        grid = create_grid(blocked_position)
        fall_time += clock.get_rawtime()
        clock.tick()
    
        if level_time/1000 > 5: 
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005
        
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            #Caso uma tecla tenho sido pressionada...
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
    
        shape_pos = convert_shape_format(current_piece)
    
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x]=current_piece.color
            
        draw_window(windown, grid, score)
        draw_next_shape(next_piece, windown)
        pygame.display.update() 
        
        if check_lost(blocked_position):
            draw_text_middle(windown, "PERDEU AMIGÃO", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
        
                        
    
def main_menu(windown):
    run = True
    while run:
        windown.fill((0,0,0))
        draw_text_middle(windown, 'Pressione qualquer tecla', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(windown)

    pygame.display.quit()

windown = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(windown)  # inicia o jogo
