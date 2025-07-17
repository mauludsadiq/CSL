import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigs

def create_hex_graph(m=5, n=5):
    return nx.hexagonal_lattice_graph(m, n)

def compute_laplacian_modes(G, k=30):
    L = nx.laplacian_matrix(G).astype(float)
    vals, vecs = eigs(L, k=k)
    phi = {j: vecs[:, j] for j in range(k)}
    return np.real(vals), phi
