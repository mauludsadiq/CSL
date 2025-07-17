import matplotlib.pyplot as plt
from collapse_script import mutate
from collapse_trace import compute_entropy
from expressions import Expression
import os

def entropy_series(expr, steps=20, prob=0.2, name="entropy_P"):
    os.makedirs("entropy_frames", exist_ok=True)
    history = []
    current = expr
    for i in range(steps):
        H = compute_entropy(current)
        history.append(H)
        current = mutate(current, prob)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(range(steps), history, marker="o")
    ax.set_title(f"Entropy Over Time ({name})")
    ax.set_xlabel("Step")
    ax.set_ylabel("Entropy (bits)")
    plt.savefig(f"entropy_frames/{name}.png")
    print(f"📈 Entropy plot saved to entropy_frames/{name}.png")
