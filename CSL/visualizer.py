# CSL/visualizer.py

import matplotlib.pyplot as plt

def plot_entropy_gamma(vm, steps=100):
    ent, align = [], []
    for _ in range(steps):
        ent.append(vm.entropy())
        align.append(vm.validator_alignment())
        vm.evolve()
    plt.plot(ent, label="Entropy H[Ψ]")
    plt.plot(align, label="Validator γ[Ψ]")
    plt.xlabel("Step")
    plt.legend()
    plt.title("Collapse Evolution")
    plt.show()
