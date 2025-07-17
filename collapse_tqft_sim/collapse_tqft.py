import jax
import jax.numpy as jnp
import numpy as np
from jax import random

# Step 1: Approximate triangulation of CP^2 (via noisy S^2)
def generate_cp2_triangulation(n=5):
    phi = jnp.linspace(0, jnp.pi, n)
    theta = jnp.linspace(0, 2 * jnp.pi, n)
    phi, theta = jnp.meshgrid(phi, theta)
    x = jnp.sin(phi) * jnp.cos(theta)
    y = jnp.sin(phi) * jnp.sin(theta)
    z = jnp.cos(phi)
    points = jnp.stack([x.flatten(), y.flatten(), z.flatten()], axis=-1)
    vertices = points + 0.1 * random.normal(random.PRNGKey(0), points.shape)
    N = vertices.shape[0]
    edges = [(i, (i + 1) % N) for i in range(N)]
    triangles = [(i, (i + 1) % N, (i + 2) % N) for i in range(N - 2)]
    return vertices, edges, triangles

# Step 2: Collapse Action
def action(g, psi, triangles):
    S = 0.0
    for (i, j, k) in triangles:
        area = jnp.linalg.norm(jnp.cross(g[j] - g[i], g[k] - g[i]))
        coupling = jnp.real(jnp.vdot(psi[i], psi[j]) + jnp.vdot(psi[j], psi[k]) + jnp.vdot(psi[k], psi[i]))
        S += area * coupling
    return S

# Step 3: Dirac-like operator
def dirac_operator(g, psi, edges):
    D = []
    for i, j in edges:
        gij = g[i] - g[j]
        D.append(jnp.outer(psi[i], jnp.conj(psi[j])) * jnp.dot(gij, gij))
    return jnp.array(D)

# Step 4: Z(CP^2) measure
def measure_Z(g, psi, triangles, edges):
    S = action(g, psi, triangles)
    D = dirac_operator(g, psi, edges)
    D = D + 1e-6 * jnp.eye(2)  # numerical stability
    det_logs = [jnp.linalg.slogdet(D[i % D.shape[0]])[1] for i in range(len(D))]
    total_logdet = jnp.sum(jnp.array(det_logs))
    exponent = -S + total_logdet
    Z_val = jnp.exp(exponent)
    print(f"S = {S:.3f}, logdet = {total_logdet:.3f}, exp = {exponent:.3f}, Z = {Z_val:.3e}")
    return Z_val

# Step 5: Simulation loop
def run_simulation(samples=25):
    key = random.PRNGKey(42)
    vertices, edges, triangles = generate_cp2_triangulation()
    g = random.normal(key, vertices.shape)
    psi = random.normal(key, (vertices.shape[0], 2)) + 1j * random.normal(key, (vertices.shape[0], 2))
    Zs = []
    for _ in range(samples):
        key, subkey = random.split(key)
        g += 0.01 * random.normal(subkey, g.shape)
        psi += 0.01 * (random.normal(subkey, psi.shape) + 1j * random.normal(subkey, psi.shape))
        Z = measure_Z(g, psi, triangles, edges)
        Zs.append(Z)
    Zs = jnp.log(jnp.array(Zs))
    print(f"\n✅ Z(CP^2) Mean: {jnp.mean(Zs):.5f}, Std: {jnp.std(Zs):.5f}")

# Execute
run_simulation()
