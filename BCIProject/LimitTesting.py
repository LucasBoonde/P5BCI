import numpy as np
import scipy.io
import matplotlib.pyplot as plt

arr1 = np.array([1,2,3,4,5,6,7,8,9,10])
arr2 = np.array([10,9,8,7,6,5,4,3,2,1])
color = np.array([1,2,2,2,2,1,1,2,2,1])

plt.scatter(arr1, arr2, c=color, cmap='bwr_r')
plt.show()





