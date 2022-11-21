import pygame, random, time
import screen_utils as Screen
from Tetris.constants import *
from Tetris.tetris import Tetris
from Tetris.commands import *

pygame.display.set_caption('Tetris')

def run_simulation():
    t = Tetris()
    while t.game_running and not t.game_over:
        chosenMove = random.choice(mapPossibleMoves(t.grid, t.blocked_pos, t.current_piece))
        rotation = chosenMove[0][0]
        posX = chosenMove[0][1]
        print(posX)
        t.main()
        time.sleep(0.2)
        
        while t.current_piece.rotation != rotation:
            if t.game_over: break
            t.main(DO_ROTATE)
            time.sleep(0.1)
            
        while posX != min([x for x, i in t.current_piece.getFormatedShape()]):
            if t.game_over: break
            if posX < min([x for x, _ in t.current_piece.getFormatedShape()]):
                t.main(GO_LEFT)                
            else:
                t.main(GO_RIGHT)
            time.sleep(0.1)
            
        t.main(PRESS_DOWN)
        t.main()
        time.sleep(0.25)
                    
    t.game_running = False 
    pygame.display.update() 
    main()

def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    surface.fill((0,0,0))
    Screen.draw_text_middle(surface, "Pressione qualquer tecla", 60, (255,255,255))
    pygame.display.update()
    
    display = True
    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
            if event.type == pygame.KEYDOWN:
                display = False
                pygame.display.quit()
                run_simulation()
    pygame.display.quit()

        
    
main()
        
        
        
    