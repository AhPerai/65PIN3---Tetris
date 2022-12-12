import pygame, random, time, math, numpy as np
import screen_utils as screen
from Tetris.constants import *
from Tetris.tetris import Tetris
from Utils.possible_moves import mapPossibleMoves, get_best_move
from  Genetic_algo.Factories.SelectionMethodFactory import *
from Genetic_algo.Factories.CrossoverMethodFactory import *
from Genetic_algo.Factories.MutationMethodFactory import *
import Genetic_algo.genetic_algorithm
import Genetic_algo.parameters 

pygame.display.set_caption('Tetris')

initial_gen  = 0
best_fitness = np.NINF
best_individual = None
population = None
n_gererations = 50 
run = 0
n_runs = 3
max_score = 1000000
gen_index = initial_gen

selection_method = RouletteWheelSelection()
crossover_method = LinearCrossover()
mutation_method =  PerturbationMutation()

def start_simulation():
    global gen_index, run, n_runs, best_fitness, best_individual, population

    #Iniciar loop de geração
    for i in range(initial_gen, initial_gen+n_gererations):
        
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
            print(population.fitnesses)
            fitness_score = 0
            
            #Cada individuo tem direito a três jogatinas
            while run < n_runs:
                result = run_game(model)
                
                fitness_score += result[0]
                run+=1
                
            #Encerra as tentativas do Individuo e calcula  o avg_fitness     
            model.fitness = round(fitness_score/3) 
            population.fitnesses[gen_index] = model.fitness
            run = 0
            #Verifica se os resultados obtidos são melhores do que o melhor já encontrado
            if model.fitness > best_fitness:
                best_fitness = model.fitness
                best_individual = model
            
        gen_index += 1
        # - TODO - Salva os dados de cada modelo da Geração em um arquivo 
         
    
def run_game(model):
    #Inicializando Tetris
    info = gen_index, run, model
    t = Tetris(info)
    while t.game_running and not t.game_over and t.score < max_score :
        #Decisão de movimento por parte do Modelo em questão
        best_move = get_best_move(model, mapPossibleMoves(t.grid, t.current_piece))
        rotation = best_move[0][0]
        posX = best_move[0][1]
        
        #Roda um frame do jogo por um breve momento 
        t.main()
        time.sleep(0.2)
        
        #Obtem a rotação desenhada 
        while t.current_piece.rotation != rotation:
            if t.game_over: break
            t.main(DO_ROTATE)
            time.sleep(0.1)

        #Obtem a posição X desejada
        while posX != min([x for x, i in t.current_piece.getFormatedShape()]):
            if t.game_over: break
            if posX < min([x for x, _ in t.current_piece.getFormatedShape()]):
                t.main(GO_LEFT)                
            else:
                t.main(GO_RIGHT)
            time.sleep(0.1)
        
        #Solta a peça, roda um frame do jogo por um breve momento   
        t.main(PRESS_DOWN)
        t.main()
        time.sleep(0.25)

    #Finaliza o jogo e atualiza a tela
    t.game_running = False 
    pygame.display.update() 
    
    #Retorna as informações apropriada da jogatinha
    return t.score, t.lines_cleared

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
        
        
        
    