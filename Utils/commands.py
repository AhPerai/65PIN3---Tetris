def goLeft(piece, grid): 
    piece.x -= 1
    if not(piece.isInValidSpace(grid)): piece.x += 1 
    
def goRight(piece, grid): 
    piece.x += 1
    if not(piece.isInValidSpace(grid)): piece.x -= 1
    
def goDown(piece, grid):
    piece.y += 1
    if not(piece.isInValidSpace(grid)): piece.y -= 1
    
def doRotate(piece, grid): 
    piece.rotation += 1
    if not(piece.isInValidSpace(grid)): piece.x -= 1