import pygame
import Tetris.tetris as Tetris

windown = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
Tetris.main_menu(windown)  # inicia o jogo

def main():
    t = Tetris()
    
    while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                t.game_running = False
                pygame.display.quit()
                quit()
    