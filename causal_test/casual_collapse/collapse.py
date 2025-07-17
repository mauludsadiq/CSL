# causal_collapse/causal_collapse/collapse.py

import networkx as nx

def now_collapse(G):
    """
    Collapse all nodes to a single node t_0 (NOW-collapse morphism).
    """
    t0 = nx.DiGraph()
    t0.add_node('t_0')
    return t0, {node: 't_0' for node in G.nodes}
