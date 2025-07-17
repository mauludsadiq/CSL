# causal_collapse/causal_collapse/sprinkling.py

import numpy as np

def kruskal_sprinkle(n, U_range=(-1,0), V_range=(0,1)):
    """
    Sprinkle n points uniformly in Kruskal-Szekeres (U, V) coordinates.
    U < 0, V > 0 covers the exterior region (r > 2M) near the horizon.
    """
    U = np.random.uniform(U_range[0], U_range[1], n)
    V = np.random.uniform(V_range[0], V_range[1], n)
    return np.column_stack((U, V))
