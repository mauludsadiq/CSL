import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# === Adaptive damping function ===
def gamma_adaptive(s_q, s_a, base_gamma=0.1):
    error_q = abs((s_q - 100) / 100)
    error_a = abs(s_a - 1)
    return base_gamma * (1 + 0.5 * max(error_q, error_a))

# === Dynamics with adaptive damping ===
def adaptive_dynamics(state, t):
    s_q, s_a, p_q, p_a = state
    gamma = gamma_adaptive(s_q, s_a)
    ds_q_dt = p_q
    ds_a_dt = p_a
    dp_q_dt = -0.2 * (s_q - 100) - gamma * p_q
    dp_a_dt = -0.2 * (s_a - 1) - gamma * p_a
    return [ds_q_dt, ds_a_dt, dp_q_dt, dp_a_dt]

# === Simulation time
t = np.linspace(0, 50, 1000)  # shorter total time

# === Initial state
initial_state = [150, -0.8, 0, 0]

# === Solve ODE
solution = odeint(adaptive_dynamics, initial_state, t)
s_q, s_a, p_q, p_a = solution[:, 0], solution[:, 1], solution[:, 2], solution[:, 3]
U = 0.1 * ((s_q - 100)**2 + (s_a - 1)**2)

# === Find stabilization time
epsilon, delta = 0.1, 0.01
stable_idx = np.where((np.abs(s_q - 100) < epsilon) & (np.abs(s_a - 1) < epsilon) &
                      (np.abs(p_q) < delta) & (np.abs(p_a) < delta) & (U < 0.01))[0]
T_stable = t[stable_idx[0]] if stable_idx.size > 0 else np.inf
print(f"🟢 Stabilization Time with Adaptive Damping: {T_stable:.2f} seconds")

# === Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Panel 1: State variables
ax1.plot(t, s_q, label='Qasim $s_Q(t)$', color='blue')
ax1.plot(t, s_a, label='Azim $s_A(t)$', color='red')
ax1.axhline(100, linestyle=':', color='blue')
ax1.axhline(1, linestyle=':', color='red')
ax1.axvline(T_stable, linestyle='--', color='green', label=f'Stable at t={T_stable:.1f}s')
ax1.set_title("State Trajectories")
ax1.set_xlabel("Time")
ax1.set_ylabel("States")
ax1.legend()
ax1.grid(True)

# Panel 2: Potential Energy
ax2.plot(t, U, label='Energy $U(t)$', color='purple')
ax2.axhline(0.01, linestyle=':', color='black')
ax2.axvline(T_stable, linestyle='--', color='green')
ax2.set_title("Potential Energy")
ax2.set_xlabel("Time")
ax2.set_ylabel("U(t)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
