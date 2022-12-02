import numpy as np
import random
from Genetic_algo.utils import getEnviromentInfo

#00: Definindo Parametros para o Indivíduo 
min_weight = -1
max_weight = 1

#Definição do Indivíduo 
class Individual():
    id: int 
    weights : list
    fitness: int
    def __init__(self, id, weights = None):
        self.id = id_num
        self.fitness = 0
        if weights == None: 
            self.weights = [random.uniform(min_weight,max_weight) for i in range(5)]
        self.weights = weights
    
    #Função para calcular o valor de cada jogada 
    def calculate(inputs):
        for i in range(5):
            score += self.weights[i] * inputs[i] 
            
        return score 
    
#00: Definindo Parametro para o Algoritmo Genético
elitism = 0.2
mutation_chance = 0.1
mutation_effectiviness = 0.1
base_pop_size = 50
offspring_rate = 1

# - Definindo Algoritmo Genético
class Population():
    self.previous_population : list
    self.population : list
    self.size : int
    self.generation: int
    def __init__(self, previous_population = None, generation):
        self.size = get_number_offsprings()
        
        #01 - Fase de Inicialização da População
        if self.previous_population == None:
            for i in range(self.size):
                id_num = (generation * size) + i 
                self.population.append(Individual(id_num))
        else:
            self.previous_population = previous_population.population
            self.population = []
            self.crossover()
            self.mutation()
            
    
    def crossover():
        #02 - Fase de Seleção de pais
        
        # Seleção de pais pela roleta
        wheel = generate_wheel(self.previous_population)
        first_parent = roullete_wheel_selection(wheel)
        second_parent = roullete_wheel_selection(wheel)
            
            
        previous_population.population.
        
    def mutation():
        
    def get_number_offsprings():
        if(self.previous_population):
            self.size =  math.ceil(offspring_rate * population_size/2)*2 
        else:
            self.size = base_pop_size      
        

# ESTÁGIO DE SELEÇÃO - Seleção por roleta 
def generate_wheel(model_population : Population):
    agg_fitness = np.sum(model_population)
    pct_fitness = np.zeros(model_population.size, dtype=int)
    
    for i in range(model_population.size):
        pct_fitness[i] = float(model_population.population[i].fitness/agg_fitness)
    
    return pct_fitness = np.cumsum(pct_fitness)
             
def roullete_wheel_selection(wheel):
    r = random.uniform(0,1)

    for i in range(wheel.size):
        if r <= wheel[i]:
            return wheel[i]
            
        
#Class Population

    #def crossover
    #def mutate 
    
#def avaliate: Dados os inputs calcula o valor de um movimento 



        