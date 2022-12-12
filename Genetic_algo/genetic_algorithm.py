import numpy as np, random
from abc import ABC, abstractmethod
from Utils.game_state import getEnviromentInfo
from Genetic_algo.Factories import *
from Genetic_algo.parameters import *


#Definição do Indivíduo 
class Individual():
    id: int 
    fitness: int
    weights : list
    def __init__(self, id, weights = None):
        self.id = id
        self.fitness = 0
        if weights == None: 
            self.weights = np.random.uniform(MIN_WEIGHT, MAX_WEIGHT, N_WEIGHTS)
        else:
            self.weights = weights
    
    #Função para calcular o valor de cada jogada 
    def calculate(self, inputs):
        score = 0
        print('pesos:',self.weights)
        for i in range(N_WEIGHTS):
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
    population : list
    fitnesses : list
    size : int
    generation: int
    def __init__(self,  
                 generation,
                 selection_method, 
                 crossover_method,
                 mutation_method,
                 previous_population = None):
        self.population = []
        self.generation = generation
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method  = mutation_method
        
        #01 - Fase de Inicialização da População
        if previous_population == None:
            self.size = POP_SIZE  
            self.fitnesses = np.zeros(self.size)
            for i in range(self.size):
                id_num = (self.generation * self.size) + i 
                self.population.append(Individual(id_num))
        else:
            self.size =  math.ceil(OFFSPRING_RATE * previous_population.size/2)*2 
            self.generate_population()
    
    def generate_population():
        self.fitnesses = np.zeros(self.size)        
        while(len(self.population) < self.size):
            self.generate_offsprings()
    
    
    def generate_offsprings():
        counter = 0
        #02 - Fase de Seleção
        parents = selection_method.execute_selection(previous_population)
        
        #03 - Fase de cruzamento 
        c_weights = crossover_method.execute_crossover(parents)
        
        #04 - Fase de mutação e por fim criação do Indivíduo 
        for children in c_weights:
            counter+=1    
            Individual(counter, mutation_method.execute_mutation())
              
        



        