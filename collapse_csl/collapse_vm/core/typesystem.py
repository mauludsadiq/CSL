def validate_type(expr):
    indices = {a.index for a in expr.anchors}
    if 4 in indices and 5 in indices:
        raise TypeError("TypeExclusionError: X₄ and X₅ may not co-occur.")
    return True
