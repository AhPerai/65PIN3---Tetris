from Genetic_algo.genetic_algorithm import *
from abc import ABC, abstractmethod

class CrossoverMethodFactory():
    
    def __init__(self, crossover_type : int):
        self.type = crossover_type        

class BaseCrossover():
    
    @abstractmethod
    def execute_crossover(self, parentes):
        pass

class UniformCrossover(BaseCrossover):
    
    def __init__(self):
        self.method_name = 'UniformCrossover'
    
    def execute_crossover(self, parents):
        p1 = parents[0]
        p2 = parents[1] 
        b = 0.2
        
        alpha = np.random.uniform(-b, 1+b, len(p1.weights))
        c1_weights = alpha*p1.weights + (1 - alpha)*p2.weights
        c2_weights = alpha*p2.weights + (1 - alpha)*p1.weights
        return np.array([c1_weights, c2_weights])
    
class LinearCrossover(BaseCrossover):
    
    def __init__(self):
        self.method_name = 'LinearCrossover'
    
    def execute_crossover(self, parents):    
        p1 = parents[0]
        p2 = parents[1] 
        c1_weights = 0.5*p1.weights + 0.5*p2.weights
        c2_weights = 1.5*p1.weights - 0.5*p2.weights
        c3_weights = 0.5*p1.weights + 1.5*p2.weights
        
        line = np.array([c1_weights, p1.weights, c2_weights, p2.weights, c3_weights])    
        rows, cols = line.shape
        child = np.random.choice(rows, 2, replace = False)
        
        c1_weights = line[child[0]]
        c2_weights = line[child[1]]
        return np.array([c1_weights, c2_weights])
    
class SimulatedBinaryCrossover(BaseCrossover):
    
    def __init__(self):
        self.method_name = 'SimulatedBinaryCrossover'
    
    def execute_crossover(self, parents):
        p1 = parents[0]
        p2 = parents[1] 
        
        DISTRIBUTION_INDEX = 5
        u = random.uniform(0, 1)
        distribution = 1/(DISTRIBUTION_INDEX + 1) 
        beta = None
        
        if u <= 0.5:
            beta = pow((2*u), distribution)
        else: 
            beta = pow((0.5*(1-u)), distribution)
            
        c1_weights = 0.5*((1+beta)*p1.weights + (1-beta)*p2.weights)
        c2_weights = 0.5*((1-beta)*p1.weights + (1+beta)*p2.weights)
        
        return np.array([c1_weights, c2_weights])