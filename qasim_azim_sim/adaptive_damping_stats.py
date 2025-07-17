import numpy as np
from scipy.integrate import odeint

# === Adaptive damping ===
def gamma_adaptive(s_q, s_a, base_gamma=0.1):
    error_q = abs((s_q - 100) / 100)
    error_a = abs(s_a - 1)
    return base_gamma * (1 + 0.5 * max(error_q, error_a))

# === Dynamics
def adaptive_dynamics(state, t):
    s_q, s_a, p_q, p_a = state
    gamma = gamma_adaptive(s_q, s_a)
    ds_q_dt = p_q
    ds_a_dt = p_a
    dp_q_dt = -0.2 * (s_q - 100) - gamma * p_q
    dp_a_dt = -0.2 * (s_a - 1) - gamma * p_a
    return [ds_q_dt, ds_a_dt, dp_q_dt, dp_a_dt]

# === Time range
t = np.linspace(0, 150, 2000)

# === Initial state
initial_state = [150, -0.8, 0, 0]

# === Solve system
solution = odeint(adaptive_dynamics, initial_state, t)
s_q, s_a = solution[:, 0], solution[:, 1]
p_q, p_a = solution[:, 2], solution[:, 3]
U = 0.1 * ((s_q - 100)**2 + (s_a - 1)**2)

# === Stabilization check
epsilon, delta = 0.1, 0.01
stable_idx = np.where(
    (np.abs(s_q - 100) < epsilon) &
    (np.abs(s_a - 1) < epsilon) &
    (np.abs(p_q) < delta) &
    (np.abs(p_a) < delta) &
    (U < 0.01)
)[0]

T_stable = t[stable_idx[0]] if stable_idx.size > 0 else np.inf

# === Collapse detection (energy spike drops)
dU_dt = np.gradient(U, t)
collapse_idx = np.where(dU_dt < -0.1 * U)[0]
collapse_times = t[collapse_idx]

# === Print diagnostics
print(f"🔢 Total Simulation Time: {t[-1]:.1f} seconds")
print(f"🟢 Stabilization Time: {T_stable:.2f} seconds")
print(f"📉 First 5 Energy Collapse Times: {collapse_times[:5]}")

# === Snapshot of final state
print("\n📊 Final State Snapshot:")
print(f"  s_q = {s_q[-1]:.4f}  (target = 100)")
print(f"  s_a = {s_a[-1]:.4f}  (target = 1)")
print(f"  p_q = {p_q[-1]:.6f}  (→ 0)")
print(f"  p_a = {p_a[-1]:.6f}  (→ 0)")
print(f"  U   = {U[-1]:.8f}    (→ 0)")
