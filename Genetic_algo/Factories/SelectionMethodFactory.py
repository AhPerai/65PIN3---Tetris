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
class RouletteWheelSelection(BaseSelection):
    current_gen : int
    
    def __init__(self):
        self.method_name = 'RouletteWheelSelection'
        self.current_gen = 0
        self.wheel = None
    
    #  - Seleção por roleta
    def generate_wheel(self, base_population):
        pop_size = base_population.size
        agg_fitness = np.sum(base_population.fitnesses)
        pct_fitness = np.zeros(pop_size)
        
        for i in range(pop_size):
            pct_fitness[i] = base_population.population[i].fitness/agg_fitness
        
        self.wheel = np.cumsum(pct_fitness)
                
    def roullete_wheel_selection(self):
        roulete = np.argwhere(self.wheel > random.uniform(0,1))[0][0]
        return roulete
    
    def execute_selection(self, base_population : Population):
        if self.wheel is None or base_population.generation != self.current_gen:
            self.generate_wheel(base_population)
            self.current_gen = base_population.generation
        
        p1 = base_population.population[self.roullete_wheel_selection()]
        p2 = base_population.population[self.roullete_wheel_selection()]
        
        return p1, p2
    
class TournamentSelection(BaseSelection):
    
    def __init__(self):
        self.method_name = 'TournamentSelection'
    
    def execute_selection(self, base_population : Population):
        parents = []
        minvalue = math. floor(base_population.size * 0.2)
        maxvalue = math. floor(base_population.size * 0.35)
        
        for i in range(2):
            parent = []
            choises = random.sample(range(base_population.size), random.randint(minvalue, maxvalue))
            for n in choises:
                parent.append(base_population.population[n])
            parent = sorted(parent, key=lambda individual: individual.fitness, reverse=True)
            parents.append(parent[0])
            
        return parents[0], parents[1]
    
class RandomSelection(BaseSelection):
    
    def __init__(self):
        self.method_name = 'RandomSelection'
    
    def execute_selection(self, base_population : Population):
        pos = []
        for i in range(2):
            pos.append(random.randrange(base_population.size))
        
        p1 = base_population.population[pos[0]]
        p2 = base_population.population[pos[1]]

        return p1, p2
            