import matplotlib.pyplot as plt
import networkx as nx
import os

# Create outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Initialize a directed graph
G = nx.DiGraph()

# Add nodes for diamond causal set
nodes = ['a', 'b', 'c', 'd', 't0']
G.add_nodes_from(nodes)

# Causal relations (solid arrows, blue)
G.add_edge('a', 'b')
G.add_edge('a', 'c')
G.add_edge('b', 'd')
G.add_edge('c', 'd')

# Positions for diamond shape
pos = {
    'a': (0, 3),
    'b': (-0.8, 2),
    'c': (0.8, 2),
    'd': (0, 1),
    't0': (4, 1.5)
}

# Create figure
fig, ax = plt.subplots(figsize=(8,5))

# Draw nodes
nx.draw_networkx_nodes(G, pos, nodelist=['a','b','c','d'], node_color='lightgray', node_size=700, edgecolors='black')
nx.draw_networkx_nodes(G, pos, nodelist=['t0'], node_color='lightgray', node_size=700, edgecolors='black')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=14, font_color='black')

# Draw causal relations (solid blue arrows)
nx.draw_networkx_edges(G, pos, edgelist=[('a','b'),('a','c'),('b','d'),('c','d')],
                       edge_color='blue', arrows=True, arrowsize=25, width=2)

# Draw NOW-collapse morphism (dashed red arrows) manually
for node in ['a', 'b', 'c', 'd']:
    ax.annotate("",
        xy=pos['t0'], xycoords='data',
        xytext=pos[node], textcoords='data',
        arrowprops=dict(arrowstyle="->", linestyle='dashed', color='red', lw=2),
    )

# Add set labels
ax.text(-1.4, 1.5, r"$\mathbb{T}$", fontsize=16, ha='center')
ax.text(4.4, 1.5, r"$\{ t_0 \}$", fontsize=16, ha='center')
ax.text(2, 3.3, r"$f$", fontsize=16, ha='center')

# Add legend
ax.plot([],[], color='blue', lw=2, label='Causal relation')
ax.plot([],[], color='red', lw=2, linestyle='dashed', label='NOW-collapse')
ax.legend(loc='lower right', fontsize=12)

# Hide axes
ax.set_axis_off()
plt.tight_layout()

# Save outputs
plt.savefig("outputs/diamond_now_collapse.png", dpi=300)
plt.savefig("outputs/diamond_now_collapse.svg")
plt.show()
