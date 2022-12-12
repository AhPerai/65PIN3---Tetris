from abc import ABC, abstractmethod
import random
import Genetic_algo.genetic_algorithm 
import  Genetic_algo.parameters 

class MutationMethodFactory():
    
    def __init__(self, mutation_type : int):
        self.type = mutation_type
    
    
class BaseMutation():
    
    @abstractmethod    
    def execute_mutation(self, offspring_weights):
        pass

class PerturbationMutation(BaseMutation):
    
    def execute(self, offspring_weights):
        flag = np.random.rand(N_WEIGHTS) <= MUTATION_RATE
        ind = np.argwhere(flag) 
        offspring_weights[ind] += round(random.uniform(-0.25, 0.25), 2)
        verify_bounds(offspring_weights)
        
        return offspring_weights



def verify_bounds(offspring_weights):
    offspring_weights = np.maximum(offspring_weights, MIN_WEIGHT)
    offspring_weights = np.minimum(offspring_weights, MAX_WEIGHT)
