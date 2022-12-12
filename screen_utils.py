from Tetris.constants import *
import pygame

def draw_text_middle(surface, text, size, color):  
        font = pygame.font.SysFont("poppins", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, (TOP_LEFT_X_AXIS + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT_y_AXIS + GRID_HEIGHT/2 - label.get_height()/2))
