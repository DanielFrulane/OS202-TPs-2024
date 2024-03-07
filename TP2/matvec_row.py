# v = A.u
import numpy as np
from mpi4py import MPI

dimension = 120 # considering divisible

globalCommunications = MPI.COMM_WORLD.Dup() # initialization
rank = globalCommunications.rank
numberOfProcessor = globalCommunications.size

numberOfRowsLocal = dimension//numberOfProcessor # considering divisible
first_row  = numberOfRowsLocal * rank # where it is
A_local = np.array([ [(i+first_row+j)%dimension+1.0 for j in range(dimension)] for i in range(numberOfRowsLocal) ])

u = np.array([i+1. for i in range(dimension)])
v_local = A_local.dot(u)
v = np.empty(dimension, v_local.dtype)
globalCommunications.Allgather(v_local, v)


filename = f"Output{rank:03d}.txt"
out = open(filename, mode='w')
out.write(f"A_local = {A_local}\n")
out.write(f"u = {u}\n")
out.write(f"v_local = {v_local}\n")
out.write(f"v = {v}\n")
out.close()
