import random
import numpy as np 
shapes = [['S', "I", "O", "J", "L", 'T'], ['O', 'I', 'J', 'L', 'L', 'I', 'S', 'J', 'O']]
print(random.choice(shapes))
# p = np.array([1, 2, 3, 4, 5])
# arr = np.random.choice(p, 5, replace = False)
# print(arr)
# LOGICAL ARRAYS
# p = np.array([1, 2, 3, 4])
# fitness_score = [10, 3, 7]
# weighted_avg = [0.5, 0.25, 0.25]
# result = 0
# for i in range(len(fitness_score)):
#         result += fitness_score[i] * weighted_avg[i]
# print(result)
# r = random.uniform(0,1)
# soma = np.sum(p)

# p = np.cumsum(p/soma)
# print(p)
# print(r)
# flag = np.argwhere(p > r)[0]
# print(flag)

# for _ in range(p.size):
#     if p[_] > r:
#         print(_,p[_])
#         break
#--------------------


#  PLOTING ---------------
# import matplotlib.pyplot as plt

# print(np.random.randint(0, 1))
# x = x + t(nmax - nmin)(1 - r**((1-current_gen)/50))

# mu, sigma = 0, 0.075 # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)

# count, bins, ignored = plt.hist(s, 30, density=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#          linewidth=2, color='r')
# plt.show()
#  PLOTING ---------------

# flag = np.random.rand(5) <= 0.2
# ind = np.argwhere(flag) 
# print(ind)


# flag = 
# for i in range(wheel.size):
#     if r <= wheel[i]:
#         return wheel[i]


            # population.fitnesses = np.random.randint(low = 100, high=1000, size=POP_SIZE)
            # for i in range(POP_SIZE): 
            #     population.population[i].fitness = population.fitnesses[i]
                
            # population = Population(generation  = gen_index,
            #                 selection_method = selection_method,
            #                 crossover_method = crossover_method,
            #                 mutation_method = mutation_method,
            #                 previous_population = population)