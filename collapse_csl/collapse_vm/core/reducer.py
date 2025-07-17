from anchors import Anchor
from fractions import Fraction

def collapse(expr):
    index_sum = sum(int(a.index * float(a.alpha)) for a in expr.anchors)
    final_index = index_sum % 60
    return Anchor(final_index, Fraction(1))
