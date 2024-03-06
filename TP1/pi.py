# mpirun -n 4 python3 pi.py
import time
import numpy as np
from mpi4py import MPI

numberOfSamples = 80000000

globalCommunications = MPI.COMM_WORLD.Dup()
numberOfProcessors = globalCommunications.size
rankOfThisProcess = globalCommunications.rank

numberOfSamplesLocal = numberOfSamples//numberOfProcessors
restOfSamples = numberOfSamples%numberOfProcessors
# makes sure all samples are processed
if rankOfThisProcess < restOfSamples: numberOfSamplesLocal += 1


beginning= time.time()
# points (x,y) within [-1;1] x [-1; 1]
x = 2.0*np.random.random_sample((numberOfSamplesLocal,))-1.0
y = 2.0*np.random.random_sample((numberOfSamplesLocal,))-1.0
maskGeometryCircle = np.array(x*x+y*y<1.0)
sumOfPointsWithinCircle = np.add.reduce(maskGeometryCircle, 0)

approximationPiLocal = np.array([4.0*sumOfPointsWithinCircle/numberOfSamples], dtype=np.double)
approximationPiGlobal= np.zeros(1, dtype=np.double)
# sums results
globalCommunications.Allreduce(approximationPiLocal, approximationPiGlobal, MPI.SUM)
end = time.time()


filename = f"Output{rankOfThisProcess:03d}.txt"
out      = open(filename, mode='w')
out.write("size: " + str(numberOfProcessors) + "\n")
out.write("rankOfThisProcess: " + str(rankOfThisProcess) + "\n")
out.write(f"Time for calculating pi: {end - beginning} s\n")
out.write(f"Pi approximation. {approximationPiGlobal[0]}\n")
out.close()