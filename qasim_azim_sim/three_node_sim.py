import numpy as np
from scipy.integrate import odeint

# Improved dynamics with full coupling and stronger damping
def dynamics_improved(state, t, k=0.2, gamma=0.2,
                      alpha_qr=0.3, alpha_ar=0.3, alpha_qa=0.1):
    s_q, s_a, s_r, p_q, p_a, p_r = state

    ds_q = p_q
    ds_a = p_a
    ds_r = p_r

    dp_q = -k * (s_q - 100) - gamma * p_q - alpha_qr * (s_q - s_r) - alpha_qa * (s_q - s_a)
    dp_a = -k * (s_a - 1) - gamma * p_a - alpha_ar * (s_a - s_r) - alpha_qa * (s_a - s_q)
    dp_r = -k * (s_r - 50) - gamma * p_r - alpha_qr * (s_r - s_q) - alpha_ar * (s_r - s_a)

    return [ds_q, ds_a, ds_r, dp_q, dp_a, dp_r]

# Time vector: simulate for 300 seconds with 2000 points
t = np.linspace(0, 300, 2000)

# Initial conditions: s_q=150, s_a=-0.8, s_r=50, zero momentum
initial_state = [150, -0.8, 50, 0, 0, 0]

# Solve ODE system
solution = odeint(dynamics_improved, initial_state, t)

s_q = solution[:, 0]
s_a = solution[:, 1]
s_r = solution[:, 2]
p_q = solution[:, 3]
p_a = solution[:, 4]
p_r = solution[:, 5]

# Potential energy function
U = 0.1 * ((s_q - 100)**2 + (s_a - 1)**2 + (s_r - 50)**2)

# Define thresholds for stabilization
epsilon = 0.1
delta = 0.01
energy_threshold = 0.01

# Find stabilization time: when all states and momenta close to equilibrium & energy small
stable_indices = np.where(
    (np.abs(s_q - 100) < epsilon) &
    (np.abs(s_a - 1) < epsilon) &
    (np.abs(s_r - 50) < epsilon) &
    (np.abs(p_q) < delta) &
    (np.abs(p_a) < delta) &
    (np.abs(p_r) < delta) &
    (U < energy_threshold)
)[0]

T_stable = t[stable_indices[0]] if stable_indices.size > 0 else np.inf

# Detect collapse moments: times where energy drops sharply
dU_dt = np.gradient(U, t)
collapse_moments = t[np.where(dU_dt < -0.1 * U)[0]]

# Print summary
print(f"🔢 Total Simulation Time: {t[-1]:.2f} seconds")
if T_stable != np.inf:
    print(f"🟢 Stabilization Time: {T_stable:.2f} seconds")
else:
    print("⚠️ System did NOT stabilize within simulation time.")

print(f"📉 First 5 Energy Collapse Times: {collapse_moments[:5]}")

print("\n📊 Final State Snapshot:")
print(f"  s_q = {s_q[-1]:.4f}  (target = 100)")
print(f"  s_a = {s_a[-1]:.4f}  (target = 1)")
print(f"  s_r = {s_r[-1]:.4f}  (target = 50)")
print(f"  p_q = {p_q[-1]:.6f}  (target = 0)")
print(f"  p_a = {p_a[-1]:.6f}  (target = 0)")
print(f"  p_r = {p_r[-1]:.6f}  (target = 0)")
print(f"  U   = {U[-1]:.6f}  (target = 0)")

# Simple Qasim advice based on final s_q
if s_q[-1] > 110:
    advice = "📉 Advise: SELL"
elif s_q[-1] < 90:
    advice = "📈 Advise: BUY"
else:
    advice = "🟨 Advise: HOLD"
print(f"\n💡 Trading Advice based on s_q: {advice}")
