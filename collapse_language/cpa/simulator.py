from scipy.linalg import expm
import numpy as np
from .anchors import get_ad_matrix
from .parser import parse_expression

def simulate_expression(expr, psi_0):
    terms = parse_expression(expr)
    trajectory = [psi_0.copy()]
    psi = psi_0.copy()
    for k, t in terms:
        ad = get_ad_matrix(k)
        psi = expm(t * ad) @ psi
        trajectory.append(psi.copy())
    return psi, trajectory
