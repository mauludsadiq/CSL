import numpy as np
from scipy.special import gamma
from scipy.optimize import minimize_scalar

def r_theory(d):
    """The expected related-pair ratio in Minkowski dimension d."""
    return (gamma(d + 1) * gamma(d / 2)) / (4 * gamma(1.5 * d))

def estimate_myrheim_meyer(N, num_relations):
    """Estimate dimension from related pairs in a causal interval."""
    if N < 2 or num_relations == 0:
        return 0.0
    r_obs = num_relations / (N * (N - 1) / 2)
    def objective(d):
        return (r_theory(d) - r_obs)**2
    res = minimize_scalar(objective, bounds=(1.1, 10), method='bounded')
    return res.x

def estimate_midpoint(N_total, N_midpoint):
    """Estimate dimension using midpoint-scaling in a causal interval."""
    if N_midpoint == 0 or N_total <= 0:
        return 0.0
    ratio = N_midpoint / N_total
    return np.log(ratio) / np.log(0.5)

def find_alexandrov(events, edges, e_min, e_max):
    """Return events in the interval [e_min, e_max] and related edges."""
    interval_events = set()
    queue = [e_min]
    while queue:
        current = queue.pop()
        if current not in interval_events:
            interval_events.add(current)
            # follow outgoing edges only if they don't exceed e_max
            for u, v in edges:
                if u == current and v <= e_max:
                    queue.append(v)
    # keep only edges fully inside interval
    interval_edges = [(u, v) for u, v in edges if u in interval_events and v in interval_events]
    return list(interval_events), interval_edges

def count_related_pairs(edges):
    """Count total causal pairs (edges) inside an interval."""
    return len(edges)

def count_midpoint(events, positions, t_min, t_max):
    """Count events up to the temporal midpoint of the interval."""
    t_half = (t_min + t_max) / 2
    return sum(1 for e in events if positions[e][0] <= t_half)

# Example usage with your causal set
if __name__ == "__main__":
    # Dummy data (replace with your own causal set)
    events = list(range(50))
    positions = {e: (np.random.uniform(0, 10), np.random.uniform(0, 10)) for e in events}
    edges = [(i, j) for i in events for j in events if i < j and np.random.rand() < 0.05]

    # Choose interval endpoints
    e_min, e_max = 0, 49
    interval_events, interval_edges = find_alexandrov(events, edges, e_min, e_max)
    
    N_total = len(interval_events)
    num_rel = count_related_pairs(interval_edges)
    
    t_min, t_max = positions[e_min][0], positions[e_max][0]
    N_mid = count_midpoint(interval_events, positions, t_min, t_max)

    dim_mm = estimate_myrheim_meyer(N_total, num_rel)
    dim_mp = estimate_midpoint(N_total, N_mid)

    print("📏 Alexandrov interval dimension estimates:")
    print(f"  Total events: {N_total}")
    print(f"  Myrheim-Meyer dimension: {dim_mm:.2f}")
    print(f"  Midpoint-scaling dimension: {dim_mp:.2f}")
