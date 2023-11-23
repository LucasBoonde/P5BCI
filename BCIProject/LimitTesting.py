import numpy as np
import scipy.io
import moabb
from moabb.datasets import BNCI2014_001


arr1 = np.array([[[0],[1],[2]]])
print("Shape", arr1.shape)

sqeezed = np.squeeze(arr1, axis=0)
print("Squeeze Axis 0", sqeezed.shape)

#sqeezed = np.squeeze(arr1, axis=1)
#print("Squeeze Axis 1", arr1.shape)

sqeezed = np.squeeze(arr1, axis=2)
print("Squeeze Axis 2", sqeezed.shape)