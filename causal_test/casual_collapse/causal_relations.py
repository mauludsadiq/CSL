# causal_collapse/causal_collapse/causal_relations.py

import networkx as nx

def causal_relations_kruskal(points, epsilon=1e-8):
    """
    Construct causal set: e_i ≺ e_j if U_i < U_j and V_i < V_j (past lightcone).
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(len(points)))
    for i, (Ui, Vi) in enumerate(points):
        for j, (Uj, Vj) in enumerate(points):
            if i != j and Ui < Uj - epsilon and Vi < Vj - epsilon:
                G.add_edge(i, j)
    return G
