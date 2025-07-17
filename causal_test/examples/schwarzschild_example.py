# examples/schwarzschild_example.py

from causal_collapse.sprinkling import kruskal_sprinkle
from causal_collapse.causal_relations import causal_relations_kruskal
from causal_collapse.visualization import visualize_causal_set

points = kruskal_sprinkle(20)
G = causal_relations_kruskal(points)
visualize_causal_set(G, points, "Schwarzschild Causal Set")
