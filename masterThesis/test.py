import numpy as np

X1, X2 = np.meshgrid(np.linspace(-2, 2, 500), np.linspace(-2, 2, 500))

# objectives to optimize; minimize F1 and maximize F2
F1 = 100 * (X1 ** 2 + X2 ** 2)
F2 = (X1 - 1) ** 2 + X2 ** 2

# constraints
G1 = 2 * (X1[0] - 0.1) * (X1[0] - 0.9)
G2 = 20 * (X1[0] - 0.4) * (X1[0] - 0.6)

import matplotlib.pyplot as plt
