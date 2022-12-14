from abc import ABC, abstractmethod
import random, numpy as np
import Genetic_algo.genetic_algorithm 
from  Genetic_algo.parameters import *

class MutationMethodFactory():
    
    def __init__(self, mutation_type : int):
        self.type = mutation_type
    
    
class BaseMutation():
    
    @abstractmethod    
    def execute_mutation(self, offspring_weights, gen = None):
        pass

class PerturbationMutation(BaseMutation):
    
    def __init__(self):
        self.method_name = 'PerturbationMutation'
    
    def execute_mutation(self, offspring_weights, gen = None):
        flag = np.random.rand(N_WEIGHTS) <= MUTATION_RATE
        ind = np.argwhere(flag)
        for i in ind:
            offspring_weights[i[0]] += round(random.uniform(-0.25, 0.25), 2)
    
        return normalize(offspring_weights)

class NonUniformMutation(BaseMutation):
    
    def __init__(self):
        self.method_name = 'NonUniformMutation'
    
    def execute_mutation(self, offspring_weights, gen = None):
        T = 0
        r = random.uniform(0,1)
        b = 2 #define a não uniformidade
        pwr = pow(1 - (gen/N_GENERATIONS), b)
        delta = pow((1 - r), pwr)
        range_w = 0.5
        if random.uniform(0,1) >= 0.5: T = -1
        else: T = 1
        
        flag = np.random.rand(N_WEIGHTS) <= MUTATION_RATE
        ind = np.argwhere(flag)
        for i in ind:
            offspring_weights[i[0]] += T*(range_w)*(delta)
        
        return normalize(offspring_weights)
        
class NormalDistributionMutation(BaseMutation):
    
    def __init__(self):
        self.method_name = 'NormalDistributionMutation'
    
    def execute_mutation(self, offspring_weights, gen = None):
        flag = np.random.rand(N_WEIGHTS) <= MUTATION_RATE
        ind = np.argwhere(flag)
        sigma = 0.075 
        for i in ind:
            offspring_weights[i[0]] += np.random.normal(0, sigma)
        
        return normalize(offspring_weights)

def normalize(offspring_weights):
    max_value = abs(max(offspring_weights, key=abs))
    if max_value > 1 : 
        normalized_weights = offspring_weights/max_value
        print(normalized_weights)
        return normalized_weights
    return offspring_weights 
