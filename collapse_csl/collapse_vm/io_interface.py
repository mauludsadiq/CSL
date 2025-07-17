from fractions import Fraction

class Anchor:
    def __init__(self, index, alpha=Fraction(1, 1)):
        self.index = index
        self.alpha = Fraction(alpha)

    def __str__(self):
        return f"X[{self.index}]^{float(self.alpha)}"

    def __repr__(self):
        return f"Anchor(index={self.index}, alpha=Fraction({self.alpha.numerator}, {self.alpha.denominator}))"
