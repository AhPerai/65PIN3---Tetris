from Tetris.constants import *
from Tetris.shapes import *
from Utils.game_state import getAcceptedPositions

class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]; 
        self.rotation = 0
        
    # Retorna os valores das posições da [coluna|linha] de cada bloco da peça formatada
    def getFormatedShape(self):
        positions = [] #Posições que cada bloco ocupará 
        format = self.shape[self.rotation % len(self.shape)]
        
        #Adquire a linha coluna de cada bloco que forma a peça 
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((self.x + j, self.y + i))
    
        #Formata a linha coluna
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
    
        return positions

    #Verifica se o movimento da peça está em um espaço válido
    def isInValidSpace(self, grid):
        accepted_pos = getAcceptedPositions(grid)   
        formatted = self.getFormatedShape()
        
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
                
        return True