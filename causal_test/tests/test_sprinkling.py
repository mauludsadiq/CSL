# tests/test_sprinkling.py

from causal_collapse.sprinkling import kruskal_sprinkle

def test_kruskal_sprinkle_shape():
    points = kruskal_sprinkle(5)
    assert points.shape == (5, 2)
