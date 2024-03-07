import numpy as np
import time
from mpi4py import MPI
import sys
import itertools

globalCommunications = MPI.COMM_WORLD.Dup()
numberOfprocessors = globalCommunications.size
rank = globalCommunications.rank
name = MPI.Get_processor_name()

N = 256000

if len(sys.argv) > 1:
    N = int(sys.argv[1])

reste= N % numberOfprocessors
NLocal = N//numberOfprocessors + (1 if reste < rank else 0) # making sure all is considered

# local table values
values = np.random.randint(-32768, 32768, size=NLocal,dtype=np.int64)

filename = f"Output{rank:03d}.txt"
out      = open(filename, mode='w')
out.write(f"Nombre de valeurs locales : {NLocal}`\n")
out.write(f"Valeurs initiales : {values}\n")

debut = time.time()
values.sort() # generic local sort
# Choix des pivots pour obtenir des buckets optimisant la distribution du tableau local
step_pivots = NLocal//numberOfprocessors
pivots = np.array(values[step_pivots : : step_pivots])
pivots = pivots[:numberOfprocessors-1] # making sure all is considered for non divisible number

# Diffusion des pivots locaux sur tous les autres processeurs :
all_pivots = np.empty(numberOfprocessors*(numberOfprocessors-1),dtype=np.int64)
globalCommunications.Allgather(pivots, all_pivots)
all_pivots.sort(kind="mergesort")

# Puis on choisit le median de chaque pivot :
glob_pivots = all_pivots[numberOfprocessors//2::numberOfprocessors]

# On range les valeurs dans des seaux locaux :
local_buckets = []
## Traitement spécial pour le proc 0 :
local_buckets.append( np.array(values[values <= glob_pivots[0]]))
## Pour les buckets 1 à numberOfprocessors-1 :
for p in range(1,numberOfprocessors-1):
    local_buckets.append( np.array(values[np.logical_and(values <= glob_pivots[p],values > glob_pivots[p-1])]) )
## Traitement spécial pour le dernier proc :
local_buckets.append( np.array(values[values > glob_pivots[-1]]) )

# On collecte les seaux des divers processeurs, processeur par processeur
my_values = None
for p in range(numberOfprocessors):
    if p == rank :
        my_values = globalCommunications.gather(local_buckets[p], root=p)
    else:
        globalCommunications.gather(local_buckets[p], root=p)

sorted_loc_values = np.array(list(itertools.chain.from_iterable(my_values)),dtype=np.int64)
sorted_loc_values.sort()
fin = time.time()

out.write(f"Temps local pour le tri : {fin-debut} secondes\n")
if sorted_loc_values.shape[0] > 0:
    out.write(f"Première valeurs locale : {sorted_loc_values[0]}\n")
    out.write(f"Dernière valeurs locale : {sorted_loc_values[-1]}\n")
    out.write(f"values : {sorted_loc_values}\n")
    out.write(f"Number of local values after sorted : {sorted_loc_values.shape[0]}\n")

out.close()