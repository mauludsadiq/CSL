import numpy as np
import re
import os
from scipy.linalg import expm

# --- Anchor Role Map ---
anchor_roles = {
    1: "Origin",
    2: "Memory",
    3: "Context",
    4: "Truth",
    5: "Inversion",
    6: "Alignment",
    7: "Control",
    8: "Collapse"
}

# --- Randomized Generator (Lie algebra element) ---
def get_ad_Xk(k):
    np.random.seed(k)
    return np.random.randn(6, 6) * 0.05

# --- Parse Collapse Expression ---
def parse_expr(expr):
    pattern = r"([¬∫∂]?)[[]X_(\d+)\^([\d.]+)[]]"
    matches = re.findall(pattern, expr)
    parsed = [(mod, int(k), float(t)) for mod, k, t in matches]
    return parsed

# --- Collapse Interpreter ---
def run_collapse_vm(expr, psi_0=None):
    psi = psi_0 if psi_0 is not None else np.array([1.0, 0, 0, 0, 0, 0])
    path = parse_expr(expr)
    states = [psi.copy()]
    trace = []

    for mod, k, t in path:
        A = get_ad_Xk(k)

        if mod == "¬":    # Negation: reverse direction
            A = -A
        elif mod == "∫":  # Binding: double-integrated (stronger)
            A = A @ A
        elif mod == "∂":  # Modulation: half strength
            A = 0.5 * A

        psi = expm(t * A) @ psi
        states.append(psi.copy())
        role = anchor_roles.get(k, f"X_{k}")
        trace.append((mod, role, t))

    return states, trace

# --- Run VM and Save Output ---
if __name__ == "__main__":
    expr = "[∫X_2^1.0][¬X_4^0.9][X_8^0.4]"
    states, trace = run_collapse_vm(expr)

    os.makedirs("output", exist_ok=True)

    # Save final state
    with open("output/final_state.txt", "w") as f:
        f.write("Final Validator State Vector:\n")
        f.write(np.array2string(states[-1], precision=5))

    # Save trace log
    with open("output/trace_log.txt", "w") as f:
        f.write("Semantic Collapse Trace:\n")
        for mod, role, t in trace:
            line = f"{mod}[{role}]^{t}\n"
            f.write(line)

    print("✅ Collapse executed.")
    print("📁 Saved final state to: output/final_state.txt")
    print("📁 Saved trace log to: output/trace_log.txt")
