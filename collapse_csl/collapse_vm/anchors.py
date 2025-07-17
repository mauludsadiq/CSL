# collapse_vm/anchors.py

class Anchor:
    def __init__(self, index, alpha):
        self.index = index % 60  # Ensure it wraps into Z/60Z
        self.alpha = float(alpha)

    def __repr__(self):
        return f"X[{self.index}]^{self.alpha:.2f}"

    def to_dict(self):
        return {"index": self.index, "alpha": self.alpha}
