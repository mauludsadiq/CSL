from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class Anchor:
    index: int                # 0 ≤ index < 60
    alpha: Fraction           # Collapse weight (rational)

    def __mul__(self, other):
        assert self.index == other.index
        return Anchor(self.index, self.alpha + other.alpha)

    def inverse(self):
        return Anchor(self.index, -self.alpha)
