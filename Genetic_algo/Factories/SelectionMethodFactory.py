from Genetic_algo.genetic_algorithm import *
from abc import ABC, abstractmethod
import numpy as np, random

# ESTÁGIO DE SELEÇÃO

class SelectionMethodFactory():
    
    def __init__(self, selector_type : int):
        self.type = selector_type
        
# Interface 
class BaseSelection():
    
    @abstractmethod
    def execute_selection(self, base_population : Population):
        pass

# Implementação Concreta

# SELEÇÃO POR ROLETA --- 
class RouletteWheelSelection(BaseSelection):
    current_gen : int
    
    def __init__(self):
        self.current_gen = 0
    
    #  - Seleção por roleta
    def generate_wheel(self, base_population):
        pop_size = base_population.population.size
        agg_fitness = np.sum(base_population.fitnesses)
        pct_fitness = np.zeros(pop_size, dtype=int)
        
        for i in range(pop_size):
            pct_fitness[i] = float(population.population[i].fitness/agg_fitness)
        
        return np.cumsum(pct_fitness)
                
    def roullete_wheel_selection(self, wheel):
        return np.argwhere(wheel > random.uniform(0,1))[0]
    
    def execute_selection(self, base_population : Population):
        if len(wheel) == 0 or base_population.generation != self.current_gen:
            wheel = generate_wheel(base_population)
            self.current_gen = base_population.generation
            
        p1 = base_population.population[roullete_wheel_selection(wheel)]
        p2 = base_population.population[roullete_wheel_selection(wheel)]
        
        return p1, p2
    
class TournamentSelection(BaseSelection):
    
    def execute_selection(self):
        pass
    
class RandomSelection(BaseSelection):
    
    def execute_selection(self):
        pass