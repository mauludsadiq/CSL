#!/usr/bin/env python3
import numpy as np
import pandas as pd
import corner
import matplotlib.pyplot as plt

# === CONFIG ===
csv_file = "mcmc_chain.csv"
param_names = [r"$H_0$", r"$\Omega_m$", r"$f_{R0}$"]
truths = [70, 0.3, 0.0]

# === 1) LOAD SAMPLES ===
try:
    print(f"Loading MCMC samples from: {csv_file}")
    df = pd.read_csv(csv_file, header=None)
    samples = df.values  # shape: (N_samples, N_params) or (N_samples, N_params + chain_id)
except FileNotFoundError:
    print("CSV file not found. Generating dummy samples instead.")
    samples = np.random.multivariate_normal(
        mean=[74, 0.28, 0.0],
        cov=[[5**2, -0.2, 0.0],
             [-0.2, 0.1**2, 0.0],
             [0.0, 0.0, 0.07**2]],
        size=10000
    )

# === 2) COMPUTE POSTERIORS ===
print("\nPosterior parameter estimates (median ±1σ):")
for i, name in enumerate(param_names):
    median = np.percentile(samples[:, i], 50)
    minus1sigma = np.percentile(samples[:, i], 16)
    plus1sigma = np.percentile(samples[:, i], 84)
    err_minus = median - minus1sigma
    err_plus = plus1sigma - median
    print(f"{name}: {median:.3f} +{err_plus:.3f} -{err_minus:.3f}")

# === 3) TRACE PLOTS ===
fig, axes = plt.subplots(len(param_names), 1, figsize=(10, 2.5 * len(param_names)), sharex=True)
for i, ax in enumerate(axes):
    ax.plot(samples[:, i], alpha=0.5)
    ax.set_ylabel(param_names[i], fontsize=12)
axes[-1].set_xlabel("MCMC step", fontsize=12)
plt.tight_layout()
plt.savefig("trace_plots.png", dpi=200)
print("\nTrace plots saved as 'trace_plots.png'.")
plt.show()

# === 4) QUICK R-hat DIAGNOSTICS (requires multiple chains) ===
# Expecting last column to be integer chain ID if chains combined into one file:
if samples.shape[1] > len(param_names):
    print("\nComputing R-hat convergence diagnostics:")
    chain_ids = samples[:, -1].astype(int)
    unique_chains = np.unique(chain_ids)
    for i, name in enumerate(param_names):
        chain_means = []
        chain_vars = []
        n_per_chain = []
        for chain in unique_chains:
            chain_samples = samples[chain_ids == chain, i]
            chain_means.append(np.mean(chain_samples))
            chain_vars.append(np.var(chain_samples, ddof=1))
            n_per_chain.append(len(chain_samples))
        B = np.var(chain_means, ddof=1) * np.mean(n_per_chain)
        W = np.mean(chain_vars)
        var_hat = (1 - 1/np.mean(n_per_chain)) * W + B / np.mean(n_per_chain)
        Rhat = np.sqrt(var_hat / W)
        print(f"R-hat {name}: {Rhat:.3f}")
else:
    print("\nNote: Only one chain detected — skipping R-hat calculation.")

# === 5) CORNER PLOT ===
figure = corner.corner(
    samples[:, :len(param_names)],  # exclude chain column if present
    labels=param_names,
    truths=truths,
    show_titles=True,
    title_fmt=".3f",
    title_kwargs={"fontsize": 12},
    label_kwargs={"fontsize": 14},
    levels=[0.68, 0.95]
)
plt.savefig("corner_plot.png", dpi=200)
print("Corner plot saved as 'corner_plot.png'.")
plt.show()
