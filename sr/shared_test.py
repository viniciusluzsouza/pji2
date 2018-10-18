from shared import *
from copy import deepcopy

my_shared = SharedObj()
my_shared.set(SharedObj.MoverMovimento, 3)
print(my_shared.get(SharedObj.MoverMovimento))

my_shared.set(SharedObj.AutomaticoPosicao, (1,1))
print(my_shared.get(SharedObj.AutomaticoPosicao))

cacas = my_shared.acquire(SharedObj.InterfaceCacasAtualizadas)
my_shared.set_directly(SharedObj.InterfaceCacasAtualizadas, [(1,2), (3,3), (5,1)])
my_shared.release(SharedObj.InterfaceCacasAtualizadas)

print(my_shared.get(SharedObj.InterfaceCacasAtualizadas))