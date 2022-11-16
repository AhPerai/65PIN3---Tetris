import numpy as np

def getMatrixParams(matrix):
    
    peaks = getPeaks(matrix)
    holes = getHoles(matrix, peaks)
    
    sum_height = getSumHeights(peaks)
    n_holes = getSumHoles(holes)
    bumpiness = getBumpiness(peaks)
    n_pits = getPits(peaks)
    n_cleared_lines = getLinesCleared(matrix)

    return sum_height, n_holes, bumpiness, n_pits, n_cleared_lines 

#Função Auxiliar
def getPeaks(matrix):
    peaks = {0: 20, 1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
    
    for row in range(20): 
        for col in range(10):       
            if matrix[row][col] != (0,0,0) and row > peaks.get(col):
                peaks[col] = row
    
    return peaks
 
def getSumHeights(peaks):
    height_sum = 0 
    for i in peaks: 
        height_sum += abs(peaks[i]-20)
    
    return height_sum
    
def getBumpiness(peaks):
    bumpiness = 0
    for i in range(9):
        bumpiness += abs(peaks[i] - peaks[i+1])
    return bumpiness 
    
def getPits(peaks):
    inc = 0
    for i in peaks: 
        if i == 20: count+=1 
    return inc
        

def getLinesCleared(matrix):
    inc = 0
    for i in range(len(matrix)-1,-1,-1):
        row = matrix[i]
        if (0, 0, 0) not in row: inc += 1
    return inc

def getHoles(matrix, peaks):
    holes = []
    
    for col in range(10):
        if peaks[col] == 20: 
            holes.append(0)
        else:
            inc = 0
            for col in range(10):
                for row in range([peaks[col], 20, -1]):
                    if matrix[row][col] == (0,0,0): inc+=1
                holes.append(inc)
    return holes

def getSumHoles(holes):
    inc = 0
    for i in holes: 
        inc+= 1
    return inc
        
        
    
# def calculateMoveValue():
     
