import pygame, random, time, math
import screen_utils as Screen
from Tetris.constants import *
from Tetris.tetris import Tetris
from Utils.possible_moves import mapPossibleMoves

pygame.display.set_caption('Tetris')


best_fitness = 0 #Melhor solução já encontrada
best_individual = None
initial_gen  = 0
n_gererations = 50  
n_runs = 3
max_score = 1000000

# def run_generation(configuration):
#     gen_index += 1
#     run = 0
#     #inicia a população
#     if()
#     for i in range(population_size):
#         population.models[i]
#         while run < n_runs:

def start_simulation():
    #Iniciar População
    
    #Iniciar loop de geração
    for i in range(initial_gen, initial_gen+n_gererations):

        for model in population:
            # - TODO - Atualiza o lado direito da tela com os dados do indivíduo
            
            lines_cleared = 0
            fitness_score = 0
            
            #Cada individuo tem direito a três jogatinas
            while run < n_runs:
                result = run_game()
                
                fitness_score += result[0]
                lines_cleared += result[1]
                run+=1
                
            #Encerra as tentativas do Individuo e calcula  o avg_fitness     
            model.fitness =  fitness/3  
            run = 0
            #Verifica se os resultados obtidos são melhores do que o melhor já encontrado
            if model.fitness > best_fitness:
                best_fitness = model.fitness
                best_individual = model
            
        
        # - TODO - Salva os dados de cada modelo da Geração em um arquivo 
         
    
def run_game(model):
    #Inicializando Tetris
    t = Tetris()
    
    while t.game_running and not t.game_over and t.score < max_score :
        #Decisão de movimento por parte do Modelo em questão
        chosenMove = random.choice(mapPossibleMoves(t.grid, t.current_piece))
        rotation = chosenMove[0][0]
        posX = chosenMove[0][1]
        
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
    Screen.draw_text_middle(surface, "Pressione qualquer tecla", 60, (255,255,255))
    pygame.display.update()
    
    display = True
    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
            if event.type == pygame.KEYDOWN:
                display = False
                pygame.display.quit()
                run_game()
    pygame.display.quit()

main()
        
        
        
    