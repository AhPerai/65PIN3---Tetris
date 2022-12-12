from Genetic_algo.genetic_algorithm import *
from abc import ABC, abstractmethod

class CrossoverMethodFactory():
    
    def __init__(self, crossover_type : int):
        self.type = crossover_type        

class BaseCrossover():
    
    @abstractmethod
    def execute_crossover(self, parentes):
        pass

class LinearCrossover(BaseCrossover):
    
    def execute(self, parents):
        p1 = parents[0]
        p2 = parents[1] 
        b = 0.5
        
        alpha = np.random.uniform(b, 1+b, len(p1.weights))
        c1_weights = alpha*p1.weights + (1 - alpha)*p2.weights
        c2_weights = alpha*p2.weights + (1 - alpha)*p1.weights
        
        return np.array([c1_weights, c2_weights])
        