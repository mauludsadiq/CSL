import numpy as np

def initialize_validators(G, constant=True):
    if constant:
        return {v: 1.0 for v in G.nodes()}
    else:
        return {v: np.random.rand() for v in G.nodes()}
