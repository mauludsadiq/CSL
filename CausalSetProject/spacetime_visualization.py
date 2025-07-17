import random
import matplotlib.pyplot as plt

# === CONFIGURATION ===
n_events = 50
T, L = 10.0, 10.0  # spacetime region: t in [0,T], x in [0,L]

# === CAUSAL RELATIONS (deep causal set) ===
causal_relations = [
    (0,5),(0,8),(0,9),(1,6),(1,7),(2,7),(2,10),(3,8),(3,11),(4,9),(4,12),
    (5,13),(5,14),(6,14),(6,15),(7,15),(7,16),(8,16),(8,17),(9,17),(9,18),
    (10,18),(10,19),(11,19),(11,20),(12,20),(12,21),
    (13,22),(14,23),(15,24),(16,25),(17,26),(18,27),(19,28),(20,29),(21,30),
    (13,24),(14,25),(15,26),(16,27),(17,28),(18,29),(19,30),
    (22,31),(23,32),(24,33),(25,34),(26,35),(27,36),(28,37),(29,38),(30,39),
    (31,40),(32,41),(33,42),(34,43),(35,44),(36,45),(37,46),(38,47),(39,48),(39,49)
]

# === RANDOMLY SPRINKLE EVENTS ===
random.seed(0)  # reproducibility
positions = {}
for event in range(n_events):
    t = random.uniform(0, T)
    x = random.uniform(0, L)
    positions[event] = (t, x)

# === PLOT SETUP ===
fig, ax = plt.subplots(figsize=(10, 7))

# Plot events as points with labels
for e, (t, x) in positions.items():
    ax.plot(x, t, 'ko', markersize=4)
    ax.text(x + 0.1, t + 0.1, str(e), fontsize=6)

# Track consistency
consistent, inconsistent = [], []

# Draw arrows and check causality
for u, v in causal_relations:
    t1, x1 = positions[u]
    t2, x2 = positions[v]
    dt, dx = t2 - t1, abs(x2 - x1)

    if dt > 0 and dx <= dt:
        # Minkowski-consistent causal edge
        color = 'green'
        consistent.append((u, v))
    else:
        # Violates Minkowski causality
        color = 'red'
        inconsistent.append((u, v))

    ax.arrow(x1, t1, x2-x1, t2-t1, head_width=0.15, head_length=0.3,
             length_includes_head=True, fc=color, ec=color, alpha=0.5)

# Axes labels and styling
ax.set_xlabel("Space (x)")
ax.set_ylabel("Time (t)")
ax.set_title("Causal Set with Minkowski Causality Check\nGreen=consistent, Red=violating")
ax.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig("causal_set_causality_check.png", dpi=300)
plt.show()

# Print summary
print(f"✅ Visualization complete. See causal_set_causality_check.png in your project folder.")
print(f"✔️ Minkowski-consistent edges: {len(consistent)}")
print(f"❌ Violating edges: {len(inconsistent)}")

if inconsistent:
    print("\n⚠️ Inconsistent edges:")
    for u, v in inconsistent:
        print(f"  Edge {u} → {v}")
