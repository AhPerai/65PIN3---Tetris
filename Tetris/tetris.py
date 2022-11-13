import pygame, random
from shapes import *
from constants import *
from commands import *
from piece import Piece

pygame.font.init()

def create_grid(locked_blocks={}):
    grid = [[(0,0,0) for i in range(10)] for i in range(20)]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_blocks:
                b = locked_blocks[(j,i)]
                grid[i][j] = b
                
    return grid     

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

    surface.blit(label, (TOP_LEFT_X_AXIS + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
    x = TOP_LEFT_X_AXIS
    y = TOP_LEFT_y_AXIS
    
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (x, y + i*BLOCK_SIZE), (x + GRID_WIDTH, y+ i*BLOCK_SIZE))
        for i in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (x + i*BLOCK_SIZE, y), (x + i*BLOCK_SIZE, y + GRID_HEIGHT))
            
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

    sx = TOP_LEFT_X_AXIS + GRID_WIDTH + 50
    sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
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
    
    surface.blit(label, (TOP_LEFT_X_AXIS + GRID_WIDTH / 2 - (label.get_width()/2), 30))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #pygame.draw.rect(supericie, cor, posX, posY, width, height, fill)
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X_AXIS + j*BLOCK_SIZE, TOP_LEFT_y_AXIS+ i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            
    pygame.draw.rect(surface, (255,0,0), (TOP_LEFT_X_AXIS, TOP_LEFT_y_AXIS, GRID_WIDTH, GRID_HEIGHT), 5)
    
    draw_grid(surface, grid)
    
    font = pygame.font.SysFont('poppins', 30)
    label = font.render('Pontuação: ', 1, (255,255,255))

    sx = TOP_LEFT_X_AXIS + GRID_WIDTH + 50
    sy = TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - 100
    surface.blit(label, (sx + 25, sy + 160))

                  
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
            if not (current_piece.isInValidSpace(grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            #Caso uma tecla tenho sido pressionada...
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_LEFT: goLeft(current_piece, grid)
                if event.key == pygame.K_RIGHT: goRight(current_piece, grid)
                if event.key == pygame.K_DOWN: goDown(current_piece, grid)
                if event.key == pygame.K_UP: doRotate(current_piece, grid)
    
        shape_pos = current_piece.getFormatedShape()
    
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

windown = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(windown)  # inicia o jogo
