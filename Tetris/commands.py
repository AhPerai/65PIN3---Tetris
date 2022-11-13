import time 

def goLeft(piece, grid): 
    piece.x -= 1
    # sleep(0.1)
    if not(piece.isInValidSpace(grid)): piece.x += 1 
    
def goRight(piece, grid): 
    piece.x += 1
    # sleep(0.1)
    if not(piece.isInValidSpace(grid)): piece.x -= 1
    
def goDown(piece, grid): 
    piece.y += 1
    # sleep(0.1)
    if not(piece.isInValidSpace(grid)): piece.y -= 1
    
def doRotate(piece, grid): 
    piece.rotation += 1
    # sleep(0.1)
    if not(piece.isInValidSpace(grid)): piece.x -= 1
    

def mapPossibleMoves(grid, blocked_position, piece):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    highest_blocks = {0: 20, 1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
    for pos in blocked_position:
        i, j = pos
        if j < highest_blocks.get(i): highest_blocks[i] = j
    
    rotations = getRotationPosition(piece)
    
    for i in rotations: 
        getValidMoves(highest_blocks, accepted_pos, rotations.get(i), i)
    
    print('calculado')
    
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
        