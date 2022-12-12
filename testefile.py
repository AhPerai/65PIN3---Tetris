import random
import numpy as np 

# LOGICAL ARRAYS
p = np.array([1, 2, 3, 4])
print(p)
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

# mu, sigma = 0, 0.33 # mean and standard deviation
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