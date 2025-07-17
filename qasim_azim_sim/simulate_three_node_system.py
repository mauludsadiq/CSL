import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def dynamics(state, t, k=0.2, gamma=0.1, alpha=0.01):
    s_q, s_a, s_r, p_q, p_a, p_r = state
    ds_q, ds_a, ds_r = p_q, p_a, p_r

    dp_q = -k * (s_q - 100) - gamma * p_q - alpha * ((s_q - s_a) + (s_q - s_r))
    dp_a = -k * (s_a - 1)   - gamma * p_a - alpha * ((s_a - s_q) + (s_a - s_r))
    dp_r = -k * (s_r - 50)  - gamma * p_r - alpha * ((s_r - s_q) + (s_r - s_a))

    return [ds_q, ds_a, ds_r, dp_q, dp_a, dp_r]

t = np.linspace(0, 150, 1000)
initial_state = [150, -0.8, 80, 0, 0, 0]  # Qasim, Azim, Risk

solution = odeint(dynamics, initial_state, t)
s_q, s_a, s_r = solution[:, 0], solution[:, 1], solution[:, 2]

# Plot all three states
plt.figure(figsize=(10, 6))
plt.plot(t, s_q, label="Qasim $s_Q$", color='blue')
plt.plot(t, s_a, label="Azim $s_A$", color='red')
plt.plot(t, s_r, label="Risk $s_R$", color='orange')
plt.axhline(100, color='blue', linestyle='--')
plt.axhline(1, color='red', linestyle='--')
plt.axhline(50, color='orange', linestyle='--')
plt.xlabel("Time (s)")
plt.ylabel("State Value")
plt.title("3-Node Damped Dynamics with Coupling")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
