import numpy as np

def get_ad_matrix(seed, dim=6):
    np.random.seed(seed)
    return np.random.randn(dim, dim) * 0.1
