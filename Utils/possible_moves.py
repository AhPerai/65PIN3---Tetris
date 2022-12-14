import time, copy, numpy as np
from Utils.game_state import *
    
def mapPossibleMoves(matrix, piece):
    possiblePlays = list()
        
    accepted_pos = getAcceptedPositions(matrix)
    peaks = getPeaks(matrix)   
    rotations = getRotationPosition(piece)
    
    for i in rotations:
        possiblePlays.append(getValidMoves(matrix, peaks, accepted_pos, rotations.get(i), i))
    
    possiblePlays = [j for play in possiblePlays for j in play]
    
    return possiblePlays
    
    
def getRotationPosition(piece): 
    rotations = {}
    for rotation in range(len(piece.shape)): 
        format = piece.shape[rotation % len(piece.shape)]
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

def getValidMoves(grid, peaks, accepted_pos, shape, rotation):
    validMoves = []
    
    for i in range(10):
        newGrid = copy.deepcopy(grid)
        validMove = True
        highest_row = peaks.get(i)
        highest_col = shape[2]+i
        for j in range(i, i+shape[1]):
            if j > 9: 
                validMove = False 
                break 
            if peaks.get(j) < highest_row:
                highest_row = peaks.get(j)
                highest_col = j 
        
        if not validMove: continue
     
        base_row = 0
        for pos in shape[0]: 
            if pos[0]+i == highest_col and pos[1] > base_row: base_row = pos[1]
        
        in_grid_positions = []
        for pos in shape[0]:
            col = pos[0]+i
            row = pos[1]-base_row+(highest_row-1)
            pos = col, row
            if pos not in accepted_pos: 
                isValid = False 
                break
            in_grid_positions.append(pos)
        if not validMove: continue
        
        for pos in in_grid_positions:
            newGrid[pos[1]][pos[0]] = (192,192,192)
            
        coordenate = rotation, i        
        inputs = getEnviromentInfo(newGrid)
        
        play = coordenate, inputs
        validMoves.append(play)
    
    return validMoves


def get_score(model, move): 
    inputs = move[1]
    score =  model.calculate(inputs)
    return score

def get_best_move(model, playable_moves):
    best_val = np.NINF
    best_move = None
    print('quantidade de movimentos:',len(playable_moves))
    for move in playable_moves: 
        score = get_score(model, move)
        if score > best_val:
            best_val = score
            best_move = move[0]
            inputs = move[1]
    print('inputs best move: ',inputs)
    print('MOVE: ',move[0])
    print('SCORE',score)
    return best_move, best_val
        