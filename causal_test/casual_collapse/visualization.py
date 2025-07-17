# causal_collapse/causal_collapse/visualization.py

import matplotlib.pyplot as plt
import networkx as nx

def visualize_causal_set(G, points=None, title="Causal Set"):
    """
    Visualize causal set G with optional point layout.
    """
    pos = {i: points[i] for i in G.nodes} if points is not None else nx.spring_layout(G)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=400, arrows=True)
    plt.title(title)
    plt.xlabel('U' if points is not None else 'Layout X')
    plt.ylabel('V' if points is not None else 'Layout Y')
    plt.show()
