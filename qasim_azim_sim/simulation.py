import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
import os
import csv
from PIL import Image
import simpleaudio as sa

# === Setup directories ===
output_dir = "output"
frames_dir = os.path.join(output_dir, "frames")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(frames_dir, exist_ok=True)

# === System parameters ===
gamma = 0.1
k_q, k_a = 0.2, 0.2
s_q_eq, s_a_eq = 100, 1

# === Potential energy function
def potential_energy(s_q, s_a):
    return 0.1 * ((s_q - s_q_eq)**2 + (s_a - s_a_eq)**2)

# === Dynamics
def hamiltonian_dynamics(state, t, gamma):
    s_q, s_a, p_q, p_a = state
    ds_q_dt = p_q
    ds_a_dt = p_a
    dp_q_dt = -k_q * (s_q - s_q_eq) - gamma * p_q
    dp_a_dt = -k_a * (s_a - s_a_eq) - gamma * p_a
    return [ds_q_dt, ds_a_dt, dp_q_dt, dp_a_dt]

# === Undamped (manual) trajectory
def simulate_undamped(t_values):
    s_q_vals, s_a_vals = [], []
    for t in t_values:
        s_q = 150 * np.exp(-t) + np.sqrt(0.4**2)
        s_a = -0.8 * np.exp(-t) + np.sqrt(t)
        s_q_vals.append(s_q)
        s_a_vals.append(s_a)
    return np.array(s_q_vals), np.array(s_a_vals)

# === Time vector
t = np.linspace(0, 5, 300)

# === Simulate dynamics
initial_state = [150, -0.8, 0, 0]
solution = odeint(hamiltonian_dynamics, initial_state, t, args=(gamma,))
s_q_damped, s_a_damped = solution[:, 0], solution[:, 1]
p_q_damped, p_a_damped = solution[:, 2], solution[:, 3]
U_damped = potential_energy(s_q_damped, s_a_damped)

# === Undamped values
s_q_undamped, s_a_undamped = simulate_undamped(t)

# === Save CSV of trajectory
csv_path = os.path.join(output_dir, "trajectory_data.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["t", "s_q", "s_a", "p_q", "p_a", "U"])
    for i in range(len(t)):
        writer.writerow([t[i], s_q_damped[i], s_a_damped[i], p_q_damped[i], p_a_damped[i], U_damped[i]])

# === Static potential energy plot
s_q_grid, s_a_grid = np.meshgrid(np.linspace(80, 120, 40), np.linspace(-1, 3, 40))
H_grid = potential_energy(s_q_grid, s_a_grid)
fig_static, ax_static = plt.subplots(figsize=(8, 6))
cs = ax_static.contourf(s_q_grid, s_a_grid, H_grid, levels=20, cmap='plasma', alpha=0.8)
fig_static.colorbar(cs, ax=ax_static, label="Potential Energy $U(s)$")
ax_static.set_xlabel('State $s_Q$')
ax_static.set_ylabel('State $s_A$')
ax_static.set_title('Potential Energy Landscape')
fig_static.savefig(os.path.join(output_dir, "energy_contours.png"), dpi=300)
plt.close(fig_static)

# === Sound trigger for energy drop
def beep():
    try:
        wave_obj = sa.WaveObject.from_wave_file("/System/Library/Sounds/Glass.aiff")
        wave_obj.play()
    except:
        print("Beep!")

# === Setup figure
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(60, 155)
ax.set_ylim(-1.2, 3.2)
ax.set_xlabel('State $s_Q$')
ax.set_ylabel('State $s_A$')
ax.set_title('Live Dynamics with Momentum and Energy Drop Alerts')

# Static overlays
ax.contour(s_q_grid, s_a_grid, H_grid, levels=10, colors='gray', alpha=0.3)
ax.axhline(y=1, color='red', linestyle=':', alpha=0.6, label='$s_A=1$')
ax.axvline(x=100, color='blue', linestyle=':', alpha=0.6, label='$s_Q=100$')

# Animation elements
line_damped, = ax.plot([], [], color='green', label='Damped Trajectory')
line_undamped, = ax.plot([], [], color='purple', linestyle='--', label='Undamped Trajectory')
point_damped, = ax.plot([], [], 'go')
point_undamped, = ax.plot([], [], 'mo')
momentum_arrow = ax.quiver([], [], [], [], color='black', scale=10, width=0.005)

ax.legend()
ax.grid(True)

# === Animate frame-by-frame and save images
prev_energy = U_damped[0]

print("Saving frames...")
for i in range(len(t)):
    # Update data
    line_damped.set_data(s_q_damped[:i], s_a_damped[:i])
    line_undamped.set_data(s_q_undamped[:i], s_a_undamped[:i])
    point_damped.set_data([s_q_damped[i]], [s_a_damped[i]])
    point_undamped.set_data([s_q_undamped[i]], [s_a_undamped[i]])
    momentum_arrow.set_UVC([p_q_damped[i]], [p_a_damped[i]])
    momentum_arrow.set_offsets([[s_q_damped[i], s_a_damped[i]]])

    # Trigger beep on energy drop
    if prev_energy - U_damped[i] > 1.5:
        beep()
    prev_energy = U_damped[i]

    # Save frame
    fname = os.path.join(frames_dir, f"frame_{i:04d}.png")
    fig.savefig(fname)

# === Compile GIF
print("Compiling GIF...")
frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")])
frames = [Image.open(f) for f in frame_files]
gif_path = os.path.join(output_dir, "simulation.gif")
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=30, loop=0)

print("✅ All done! Outputs saved in 'output/' folder.")
