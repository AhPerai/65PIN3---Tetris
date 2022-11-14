SCREEN_WIDTH = 800   
SCREEN_HEIGHT = 700

BLOCK_SIZE = 30
ROWS = 20
COLS = 10

GRID_HEIGHT = BLOCK_SIZE * ROWS
GRID_WIDTH =  BLOCK_SIZE * COLS

#Auxiliares para lidar com a posicionamento
TOP_LEFT_X_AXIS = (SCREEN_WIDTH - GRID_WIDTH) / 2
TOP_LEFT_y_AXIS = SCREEN_HEIGHT - GRID_HEIGHT

SCORE_BY_LINE_CLEARED = [0, 40, 100, 300, 1200]