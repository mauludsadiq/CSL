import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Paths ===
OUTPUT_DIR = "outputs"
SAT_FILE = os.path.join(OUTPUT_DIR, "entropy_data.csv")
CURVATURE_PLOT = os.path.join(OUTPUT_DIR, "entropy_curvature.png")

# === Load Data ===
df = pd.read_csv(SAT_FILE)
n_vals = df["n"].values
H_vals = df["entropy"].values

# === First Derivative: ΔH(n) = H(n) - H(n-5) ===
delta_H = np.full_like(H_vals, np.nan, dtype=np.float64)
for i in range(len(H_vals)):
    if i >= 1:
        delta_H[i] = H_vals[i] - H_vals[i-1]

# === Second Derivative: Δ²H(n) = ΔH(n) - ΔH(n-1) ===
delta2_H = np.full_like(delta_H, np.nan, dtype=np.float64)
for i in range(len(delta_H)):
    if i >= 1 and not np.isnan(delta_H[i]) and not np.isnan(delta_H[i-1]):
        delta2_H[i] = delta_H[i] - delta_H[i-1]

# === Plot ===
plt.figure(figsize=(10, 5))
plt.axhline(0, color="gray", linestyle="--", linewidth=1)

# ΔH
plt.plot(n_vals, delta_H, marker="o", label="ΔH(n) = H(n) - H(n−1)")

# Δ²H
plt.plot(n_vals, delta2_H, marker="s", label="Δ²H(n)", linestyle="--")

plt.title("Entropy Curvature (Collapse Acceleration)")
plt.xlabel("n")
plt.ylabel("Entropy Change")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show
plt.savefig(CURVATURE_PLOT)
plt.show()
