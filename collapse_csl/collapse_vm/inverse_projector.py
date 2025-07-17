from fractions import Fraction
from anchors import Anchor

def inverse_to_cancel(target: Anchor, goal_index=0):
    # Find anchor X[m]^-b such that (k·a + m·(-b)) ≡ goal mod 60
    k, a = target.index, float(target.alpha)

    for m in range(60):
        b = (k * a - goal_index) / m if m != 0 else None
        if b and 0 < b < 5:
            print(f"To cancel X[{k}]^{a}, use X[{m}]^-{round(b,3)}")
