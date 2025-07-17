import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
import pickle

# 1) Sprinkle points uniformly in 2D Minkowski region
np.random.seed(0)
n_nodes = 500  # increased from 50 to 500
times = np.sort(np.random.uniform(0, 1, n_nodes))
spaces = np.random.uniform(-0.5, 0.5, n_nodes)
events = list(range(n_nodes))

# 2) Build causet edges: i -> j if t_j > t_i and |x_j - x_i| < t_j - t_i
G = nx.DiGraph()
for i in events:
    for j in events:
        if i < j and times[j] > times[i]:
            dt, dx = times[j] - times[i], abs(spaces[j] - spaces[i])
            if dx < dt:
                G.add_edge(i, j)
G = nx.transitive_closure(G)

# 3) Compute causal diamonds (past ∪ future sets) for each node
diamonds = []
for e in events:
    past = set(nx.ancestors(G, e))
    future = set(nx.descendants(G, e))
    diamond = past | future
    diamonds.append(diamond)

# 4) Compute similarity matrix: Jaccard overlap of causal diamonds
sim_matrix = np.zeros((n_nodes, n_nodes))
for i in events:
    for j in events:
        di, dj = diamonds[i], diamonds[j]
        inter = len(di & dj)
        union = len(di | dj) + 1e-8
        sim_matrix[i, j] = inter / union

# 5) Perform agglomerative clustering on similarity
dissimilarity = 1 - sim_matrix
linked = linkage(dissimilarity, method='average')
num_clusters = 8  # increased to account for more events
cluster_labels = fcluster(linked, num_clusters, criterion='maxclust')

# 6) Build quotient causal set
Q_edges = set()
for u, v in G.edges():
    cu, cv = cluster_labels[u], cluster_labels[v]
    if cu != cv:
        Q_edges.add((f"C{cu}", f"C{cv}"))
Q = nx.DiGraph()
Q.add_edges_from(Q_edges)

# 7) Plot original causet
plt.figure(figsize=(12,8))
pos = {e: (spaces[e], -times[e]) for e in events}  # Minkowski diagram style
nx.draw(G, pos, with_labels=False, node_size=10, arrows=False, edge_color="lightblue")
plt.title("Original 500-node Sprinkled Causet")
plt.savefig("original_500node.png", dpi=300)
plt.close()

# 8) Plot quotient causal set
plt.figure(figsize=(8,6))
q_pos = nx.spring_layout(Q, seed=1)
nx.draw(Q, q_pos, with_labels=True, node_color="violet", node_size=500, arrows=True, font_size=8)
plt.title("Quotient Graph: Causal-Diamond Clustering")
plt.savefig("quotient_diamond.png", dpi=300)
plt.close()

# 9) Compute and plot cluster volumes
cluster_sizes = {}
for lbl in np.unique(cluster_labels):
    cluster_sizes[f"C{lbl}"] = np.sum(cluster_labels == lbl)

labels = ["Original"] + list(cluster_sizes.keys())
sizes = [n_nodes] + list(cluster_sizes.values())
colors = ["gray"] + ["violet"]*len(cluster_sizes)

plt.figure(figsize=(10,5))
plt.bar(labels, sizes, color=colors)
plt.ylabel("Number of Events (Spacetime Volume)")
plt.title("Cluster Volumes: Causal-Diamond Clustering")
plt.savefig("volume_diamond.png", dpi=300)
plt.close()

# 10) Print cluster assignments
for lbl in np.unique(cluster_labels):
    members = [f"E{e}" for e in np.where(cluster_labels==lbl)[0]]
    print(f"Cluster C{lbl}: {members}")

print("\nAll plots saved as original_500node.png, quotient_diamond.png, volume_diamond.png")

# 11) SAVE CAUSAL SET DATA FOR SAMPLER
positions = {e: (times[e], spaces[e]) for e in events}
edges = list(G.edges())

data = {
    "events": events,
    "positions": positions,
    "edges": edges,
}

with open("causal_set_data.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ Causal set data saved to causal_set_data.pkl")
