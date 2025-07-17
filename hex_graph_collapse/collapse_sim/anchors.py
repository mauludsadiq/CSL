def find_anchor(phi, anchor_index=0, G=None, node_index=None):
    if G is None or node_index is None:
        raise ValueError("Graph and node_index must be provided.")
    return min(G.nodes(), key=lambda v: phi[anchor_index][node_index[v]].real)
