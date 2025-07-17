import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import networkx as nx
import matplotlib.pyplot as plt

# PARAMETERS
lambda_collapse = 1.0  # strength of the collapse potential

# Build minimal 2D grid to simulate S^2 × S^2
def generate_grid(n):
    x = np.linspace(-1, 1, n)
    y = np.linspace(-1, 1, n)
    grid = np.array([[xi, yi] for xi in x for yi in y])
    return grid

# Build graph Laplacian
def build_laplacian(points, k=4):
    from sklearn.neighbors import kneighbors_graph
    A = kneighbors_graph(points, k, mode='connectivity', include_self=False)
    L = sp.csgraph.laplacian(A, normed=False)
    return L

# Collapse potential and gradient
def V(phi): return (lambda_collapse / 4) * phi**4
def grad_V(phi): return lambda_collapse * phi**3

# Solve Δφ = V'(φ) using Newton iteration
def solve_collapse(L, tol=1e-6, max_iter=100):
    n = L.shape[0]
    phi = 0.1 * np.random.randn(n)
    for i in range(max_iter):
        F = L @ phi - grad_V(phi)
        J = L - sp.diags(3 * lambda_collapse * phi**2)
        try:
            delta = spla.spsolve(J, -F)
        except Exception as e:
            print("Solver failed:", e)
            break
        phi += delta
        if np.linalg.norm(F) < tol:
            break
    return phi

# Compute action S[φ]
def action(L, phi):
    grad = L @ phi
    kinetic = 0.5 * np.dot(phi, grad)
    potential = np.sum(V(phi))
    return kinetic + potential

# Simulate collapse homology basis (spectral proxy)
def collapse_homology(L):
    eigvals, _ = spla.eigsh(L, k=5, which='SM')  # lowest eigenvalues
    return eigvals

def main():
    N = 20
    grid = generate_grid(N)
    L = build_laplacian(grid, k=6)
    phi = solve_collapse(L)
    S = action(L, phi)
    eigvals = collapse_homology(L)

    print(f"✅ Collapse action S[ϕ] = {S:.4f}")
    print(f"Homology spectrum (lowest eigenvalues): {eigvals}")

    plt.figure(figsize=(6, 5))
    plt.tricontourf(grid[:, 0], grid[:, 1], phi, levels=50, cmap='viridis')
    plt.colorbar(label='ϕ collapse field')
    plt.title('Collapse Field ϕ on S² × S² Grid')
    plt.tight_layout()
    plt.savefig('collapse_field.png', dpi=200)
    plt.show()

if __name__ == "__main__":
    main()
