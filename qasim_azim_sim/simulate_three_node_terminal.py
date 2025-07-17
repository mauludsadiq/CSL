import numpy as np
from scipy.integrate import odeint

def dynamics(state, t, k=0.2, gamma=0.1, alpha=0.01):
    s_q, s_a, s_r, p_q, p_a, p_r = state
    ds_q, ds_a, ds_r = p_q, p_a, p_r

    dp_q = -k * (s_q - 100) - gamma * p_q - alpha * ((s_q - s_a) + (s_q - s_r))
    dp_a = -k * (s_a - 1)   - gamma * p_a - alpha * ((s_a - s_q) + (s_a - s_r))
    dp_r = -k * (s_r - 50)  - gamma * p_r - alpha * ((s_r - s_q) + (s_r - s_a))

    return [ds_q, ds_a, ds_r, dp_q, dp_a, dp_r]

# Time array and initial conditions
t = np.linspace(0, 150, 1000)
initial_state = [150, -0.8, 80, 0, 0, 0]  # s_q, s_a, s_r, p_q, p_a, p_r

# Solve ODEs
solution = odeint(dynamics, initial_state, t)
s_q, s_a, s_r = solution[:, 0], solution[:, 1], solution[:, 2]
p_q, p_a, p_r = solution[:, 3], solution[:, 4], solution[:, 5]

# Compute potential energy
U = 0.1 * ((s_q - 100)**2 + (s_a - 1)**2 + (s_r - 50)**2)

# Print final snapshot
print("\n🧮 Final System Snapshot (t = {:.2f} s)".format(t[-1]))
print(f"  s_q = {s_q[-1]:.4f}  (target = 100)")
print(f"  s_a = {s_a[-1]:.4f}  (target = 1)")
print(f"  s_r = {s_r[-1]:.4f}  (target = 50)")
print(f"  p_q = {p_q[-1]:.6f}  (→ 0)")
print(f"  p_a = {p_a[-1]:.6f}  (→ 0)")
print(f"  p_r = {p_r[-1]:.6f}  (→ 0)")
print(f"  U   = {U[-1]:.8f}    (→ 0)\n")
