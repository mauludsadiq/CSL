# CSL/plotter.py

import matplotlib.pyplot as plt
import csv

def plot_trace(csv_file):
    steps = []
    gamma = []
    entropy = []

    try:
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                steps.append(int(row["step"]))
                gamma.append(float(row["gamma"]))
                entropy.append(float(row["entropy"]))
    except Exception as e:
        print(f"[Error reading CSV] {e}")
        return

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Step")
    ax1.set_ylabel("γ[Ψ] (Validator Alignment)", color="tab:blue")
    ax1.plot(steps, gamma, label="γ[Ψ]", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("H[Ψ] (Entropy)", color="tab:red")
    ax2.plot(steps, entropy, label="H[Ψ]", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title(f"Collapse Trace: {csv_file}")
    fig.tight_layout()
    plt.show()
