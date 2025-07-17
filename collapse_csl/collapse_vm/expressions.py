# collapse_vm/expressions.py

import numpy as np
from collections import defaultdict

class Expression:
    def __init__(self, anchors):
        self.anchors = anchors
        self.index_weights = self._aggregate()

    def _aggregate(self):
        weights = defaultdict(float)
        for anchor in self.anchors:
            weights[anchor.index] += anchor.alpha
        return weights

    def collapse(self):
        if not self.index_weights:
            raise ValueError("No anchors to collapse.")
        return max(self.index_weights.items(), key=lambda item: item[1])[0]

    def __repr__(self):
        parts = [f"X[{idx}]^{alpha:.2f}" for idx, alpha in self.index_weights.items()]
        return " · ".join(parts)
