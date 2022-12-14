import pygame, random, time, math, numpy as np
import screen_utils as screen
from Tetris.constants import *
from Tetris.shapes import *
from Tetris.tetris import Tetris
from Utils.possible_moves import mapPossibleMoves, get_best_move
from  Genetic_algo.Factories.SelectionMethodFactory import *
from Genetic_algo.Factories.CrossoverMethodFactory import *
from Genetic_algo.Factories.MutationMethodFactory import *
import Genetic_algo.genetic_algorithm
import Genetic_algo.parameters 

pygame.display.set_caption('Tetris')

best_fitness = np.NINF
best_individual = None
population = None
run = 0
max_score = 1000000
gen_index = 0
weighted_avg = [0.5, 0.5]
shapes = [[S, I, O, J, L, T], 
          [J, L, T, S, I, O], 
          [J, I, O, S, L, T], 
          [J, S, L, O, I, T, L, S, J],
          [S, I, O, T, L, J, I, O, I]]

selection_method = RandomSelection()
crossover_method = UniformCrossover()
mutation_method =  NormalDistributionMutation()

def start_simulation():
    counter = 0
    best_individuals_of_generation = []
    generation_data = []
    global gen_index, run, best_fitness, best_individual, population

    #Iniciar loop de geração
    for i in range(N_GENERATIONS):
        path = f'simulations/{selection_method.method_name}/{crossover_method.method_name}/{mutation_method.method_name}/'
        #Iniciar População
        if population is None:
            population = Population(generation = gen_index, 
                                    selection_method = selection_method,
                                    crossover_method = crossover_method,
                                    mutation_method = mutation_method)
                        
        else:
            population = Population(generation  = gen_index,
                            selection_method = selection_method,
                            crossover_method = crossover_method,
                            mutation_method = mutation_method,
                            previous_population = population)

        for model in population.population:
            fitness_score = []
            
            #Cada individuo tem direito a três jogatinas
            while run < N_RUNS:
                result = run_game(model)
                
                fitness_score.append(result)
                run+=1
                
            #Encerra as tentativas do Individuo e calcula  o avg_fitness     
            for i in range(len(fitness_score)):
                 model.fitness += fitness_score[i] * weighted_avg[i]
    
            population.fitnesses[counter] = model.fitness
            run = 0
            counter+=1
            #Verifica se os resultados obtidos são melhores do que o melhor já encontrado
            if model.fitness > best_fitness:
                best_fitness = model.fitness
                best_individual = model
        
        
        for model in population.population:
            model_data = []
            model_data.append(model.id)
            for w in model.weights:
                model_data.append(w) 
            model_data.append(model.fitness)
            generation_data.append(model_data)
        
        best_individuals_of_generation.append(generation_data[np.argmax(population.fitnesses)])
        filename = f'gen{gen_index}.csv'
        np.savetxt(path+filename, generation_data, delimiter=',', fmt='%i;' + '%1.5f;'*5 + '%i;')
            
        generation_data = []
        gen_index += 1
        counter = 0
    
    np.savetxt(path+'fitnesses.csv', best_individuals_of_generation, delimiter=',', fmt='%i;' + '%1.5f;'*5 + '%i;')
         
    
def run_game(model):
    #Inicializando Tetris
    global run, shapes 
    info = gen_index, run, model
    
    if run == 0: t = Tetris(info, random.choice(shapes))
    else: t = Tetris(info)
    
    while t.game_running and not t.game_over and t.score < max_score :
        #Decisão de movimento por parte do Modelo em questão
        best_move = get_best_move(model, mapPossibleMoves(t.grid, t.current_piece))
        rotation = best_move[0][0]
        posX = best_move[0][1]
        
        #Roda um frame do jogo por um breve momento 
        t.main()
        
        #Obtem a rotação desenhada 
        while t.current_piece.rotation != rotation:
            if t.game_over: break
            t.main(DO_ROTATE)

        #Obtem a posição X desejada
        while posX != min([x for x, i in t.current_piece.getFormatedShape()]):
            if t.game_over: break
            if posX < min([x for x, _ in t.current_piece.getFormatedShape()]):
                t.main(GO_LEFT)                
            else:
                t.main(GO_RIGHT)
        
        #Solta a peça, roda um frame do jogo por um breve momento   
        t.main(PRESS_DOWN)
        t.main()

    #Finaliza o jogo e atualiza a tela
    t.game_running = False 
    pygame.display.update() 
    
    #Retorna as informações apropriada da jogatinha
    return t.score

def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    surface.fill((0,0,0))
    screen.draw_text_middle(surface, "Pressione qualquer tecla", 60, (255,255,255))
    pygame.display.update()
    
    display = True
    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
            if event.type == pygame.KEYDOWN:
                display = False
                pygame.display.quit()
                start_simulation()
    pygame.display.quit()

main()
        
        
        
    