# v = A.u
import numpy as np
from mpi4py import MPI

dimension = 120

globalCommunications = MPI.COMM_WORLD.Dup()
rank = globalCommunications.rank
numberOfProcessors = globalCommunications.size

numberOfCollumnsLocal = dimension//numberOfProcessors
first_collumn   = numberOfCollumnsLocal * rank
A_local = np.array([ [(i+j+first_collumn)%dimension+1.0 for j in range(numberOfCollumnsLocal)] for i in range(dimension) ])

u_local = np.array([i+first_collumn+1. for i in range(numberOfCollumnsLocal)])
v_partial = A_local.dot(u_local)
v = np.empty(dimension, dtype=v_partial.dtype)
globalCommunications.Allreduce(v_partial, v)


filename = f"Output{rank:03d}.txt"
out      = open(filename, mode='w')
out.write(f"A_local = {A_local}\n")
out.write(f"u_local = {u_local}\n")
out.write(f"v_partial = {v_partial}\n")
out.write(f"v = {v}\n")
out.close()
