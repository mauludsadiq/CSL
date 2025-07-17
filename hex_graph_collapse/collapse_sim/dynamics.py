import numpy as np
import math

def collapse_step(validators, phi, lambda_j, G, node_index):
    new_validators = {}
    for v in G.nodes():
        idx = node_index[v]
        decay = sum(lambda_j[j] * (phi[j][idx].real)**2 for j in range(len(lambda_j)))
        new_validators[v] = validators[v] * np.exp(-decay)
    return new_validators

def compute_entropy(validators):
    values = np.array(list(validators.values()))
    probs = values / values.sum()
    return -np.sum(probs * np.log(probs + 1e-10))

def project_modes(state_vector, phi, mode_count):
    return [np.dot(state_vector, phi[j].real) for j in range(mode_count)]
