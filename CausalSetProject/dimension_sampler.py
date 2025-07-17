import numpy as np
import random
import matplotlib.pyplot as plt
from dimension_estimators import (find_alexandrov, estimate_myrheim_meyer,
                                  estimate_midpoint, count_related_pairs,
                                  count_midpoint)

def sample_intervals(events, edges, positions, num_samples=50, min_events=20):
    dims_mm, dims_mp = [], []

    for _ in range(num_samples):
        e_min, e_max = sorted(random.sample(events, 2))
        interval_events, interval_edges = find_alexandrov(events, edges, e_min, e_max)
        N_total = len(interval_events)
        if N_total < min_events:
            continue  # skip small intervals
        num_rel = count_related_pairs(interval_edges)
        t_min, t_max = positions[e_min][0], positions[e_max][0]
        N_mid = count_midpoint(interval_events, positions, t_min, t_max)
        dim_mm = estimate_myrheim_meyer(N_total, num_rel)
        dim_mp = estimate_midpoint(N_total, N_mid)
        dims_mm.append(dim_mm)
        dims_mp.append(dim_mp)
    return dims_mm, dims_mp

if __name__ == "__main__":
    # Replace with your causal set data:
    events = list(range(200))
    positions = {e: (np.random.uniform(0, 10), np.random.uniform(0, 10)) for e in events}
    edges = [(i, j) for i in events for j in events if i < j and np.random.rand() < 0.01]

    dims_mm, dims_mp = sample_intervals(events, edges, positions, num_samples=100, min_events=20)

    print(f"Sampled {len(dims_mm)} valid intervals with ≥20 events")
    print(f"Mean Myrheim-Meyer dimension: {np.mean(dims_mm):.2f} ± {np.std(dims_mm):.2f}")
    print(f"Mean midpoint-scaling dimension: {np.mean(dims_mp):.2f} ± {np.std(dims_mp):.2f}")

    plt.figure(figsize=(10,5))
    plt.hist(dims_mm, bins=20, alpha=0.6, label="Myrheim-Meyer")
    plt.hist(dims_mp, bins=20, alpha=0.6, label="Midpoint-scaling")
    plt.xlabel("Estimated Dimension")
    plt.ylabel("Frequency")
    plt.title("Distribution of Estimated Dimensions from Random Alexandrov Intervals")
    plt.legend()
    plt.tight_layout()
    plt.savefig("dimension_distribution.png", dpi=300)
    plt.show()
