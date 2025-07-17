from anchors import Anchor
from expressions import Expression
from fractions import Fraction

def synthesize_target(index=33, count=3):
    # Spread random anchor weights to hit target collapse
    # Solve: sum(k_i * alpha_i) ≈ index
    base = [10, 15, 22]  # pre-defined indices
    total = sum(base)
    weights = [Fraction(index * 1.0 * b / total) / b for b in base]
    anchors = [Anchor(k, w) for k, w in zip(base, weights)]
    expr = Expression(anchors)
    print(f"🧪 Synthesized collapse expression for X[{index}] →")
    for a in anchors:
        print(f"• X[{a.index}]^{float(a.alpha)}")
    return expr
