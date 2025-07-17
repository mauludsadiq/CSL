from anchors import Anchor

class Expression:
    def __init__(self, anchors):
        self.anchors = self._simplify(anchors)

    def _simplify(self, anchors):
        by_index = {}
        for a in anchors:
            if a.index not in by_index:
                by_index[a.index] = a.alpha
            else:
                by_index[a.index] += a.alpha
        return [Anchor(k, a) for k, a in by_index.items() if a != 0]

    def __mul__(self, other):
        return Expression(self.anchors + other.anchors)
