import random
import numpy as np 

p = np.array([1, 2, 3, 4])
r = random.uniform(0,1)

soma = np.sum(p)

p = np.cumsum(p/soma)

print(p)
print(r)

for _ in range(p.size):
    if r <= p[_]:
        print(_,p[_])
        break