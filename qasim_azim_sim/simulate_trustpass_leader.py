import numpy as np
from scipy.integrate import odeint

def dynamics(state, t, k=0.2, gamma=0.1, alpha_qr=0.2, alpha_ar=0.2, alpha_qa=0.05):
    s_q, s_a, s_r, p_q, p_a, p_r = state

    ds_q = p_q
    ds_a = p_a
    ds_r = p_r

    # Qasim pulled by own equilibrium + TrustPass + Azim
    dp_q = -k * (s_q - 100) - gamma * p_q - alpha_qr * (s_q - s_r) - alpha_qa * (s_q - s_a)

    # Azim pulled by own equilibrium + TrustPass + Qasim
    dp_a = -k * (s_a - 1) - gamma * p_a - alpha_ar * (s_a - s_r) - alpha_qa * (s_a - s_q)

    # TrustPass pulled by own equilibrium only (strong self-stabilizer)
    dp_r = -k * (s_r - 50) - gamma * p_r

    return [ds_q, ds_a, ds_r, dp_q, dp_a, dp_r]

def potential_energy(s_q, s_a, s_r, target_q=100, target_a=1, target_r=50, coeff=0.1):
    return coeff * ((s_q - target_q)**2 + (s_a - target_a)**2 + (s_r - target_r)**2)

def simulate():
    # Time vector: 0 to 150 seconds, 1000 points
    t = np.linspace(0, 150, 1000)

    # Initial states: s_q=150 (far high), s_a=-0.8 (low), s_r=49 (near), zero momentum
    initial_state = [150, -0.8, 49, 0, 0, 0]

    # Solve ODE
    sol = odeint(dynamics, initial_state, t)

    s_q, s_a, s_r, p_q, p_a, p_r = sol.T

    # Compute potential energy
    U = potential_energy(s_q, s_a, s_r)

    # Find stabilization time where all states close to equilibrium and momentum low
    epsilon = 0.1
    delta = 0.01
    stable_idx = np.where(
        (np.abs(s_q - 100) < epsilon) &
        (np.abs(s_a - 1) < epsilon) &
        (np.abs(s_r - 50) < epsilon) &
        (np.abs(p_q) < delta) &
        (np.abs(p_a) < delta) &
        (np.abs(p_r) < delta) &
        (U < 0.01)
    )[0]

    T_stable = t[stable_idx[0]] if stable_idx.size > 0 else np.inf

    # Print final snapshot at last time step
    print(f"🎯 Final System Snapshot (t = {t[-1]:.2f} s)")
    print(f"  s_q = {s_q[-1]:.4f}  (target = 100)")
    print(f"  s_a = {s_a[-1]:.4f}  (target = 1)")
    print(f"  s_r = {s_r[-1]:.4f}  (target = 50)")
    print(f"  p_q = {p_q[-1]:.6f}  (target = 0)")
    print(f"  p_a = {p_a[-1]:.6f}  (target = 0)")
    print(f"  p_r = {p_r[-1]:.6f}  (target = 0)")
    print(f"  U   = {U[-1]:.6f}  (target = 0)")
    print()
    print(f"✅ Stabilization Time: {T_stable:.2f} seconds")

if __name__ == "__main__":
    simulate()
