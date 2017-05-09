import numpy as np
from sklearn.preprocessing import normalize

x = np.random.rand(20)*10
print(x)
norm1 = x / np.linalg.norm(x)
norm2 = 5*normalize(x[:,np.newaxis], axis=0).ravel()
print(norm2)
print(5*norm2)
