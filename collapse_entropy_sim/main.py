import numpy as np
import matplotlib.pyplot as plt
from entropy import estimate_entropy, generate_random_3cnf, apply_random_restriction

def run_entropy_sweep(n=50, num_clauses=100, trials_per_rho=20):
    rhos = np.linspace(0.5, 0.99, 10)
    mean_entropies = []
    std_entropies = []

    for rho in rhos:
        print(f"Running trials for ρ = {rho:.3f}")
        entropies = []
        for _ in range(trials_per_rho):
            formula = generate_random_3cnf(n, num_clauses)
            restricted_formula = apply_random_restriction(formula, n, rho)
            H = estimate_entropy(restricted_formula, n)
            entropies.append(H)
        mean_entropies.append(np.mean(entropies))
        std_entropies.append(np.std(entropies))

    return rhos, mean_entropies, std_entropies

def plot_entropy_vs_rho(rhos, means, stds):
    plt.errorbar(rhos, means, yerr=stds, fmt='-o', label="Entropy after restriction")
    plt.xlabel("ρ (fraction of variables *unrestricted*)")
    plt.ylabel("Entropy H(q(p))")
    plt.title("Entropy Decay vs. Restriction Strength")
    plt.grid(True)
    plt.legend()
    plt.savefig("entropy_vs_rho.png")
    plt.show()

if __name__ == "__main__":
    print("Running entropy tests with restrictions...")
    rhos, means, stds = run_entropy_sweep(n=50, num_clauses=100, trials_per_rho=20)

    print("\nResults Summary:")
    for rho, mean, std in zip(rhos, means, stds):
        print(f"ρ = {rho:.3f} → Mean Entropy = {mean:.10f}, Std Dev = {std:.10f}")

    plot_entropy_vs_rho(rhos, means, stds)
