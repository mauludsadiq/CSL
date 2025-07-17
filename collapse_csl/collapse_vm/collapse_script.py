# collapse_vm/collapse_script.py

from collections import namedtuple

Anchor = namedtuple("Anchor", ["index", "alpha"])

class CollapseEnvironment:
    def __init__(self):
        self.history = []
        self.last_expr = []

    def collapse(self, anchors):
        # Collapse logic: find anchor with max alpha
        collapse_index = max(anchors, key=lambda x: x.alpha).index
        self.last_expr = anchors
        return collapse_index

    def mutate(self, anchors, probability):
        from random import random, uniform
        mutated = []
        for anchor in anchors:
            if random() < probability:
                delta = uniform(-0.3, 0.3)
                mutated.append(Anchor(index=anchor.index, alpha=max(0.0, anchor.alpha + delta)))
            else:
                mutated.append(anchor)
        return mutated

ENV = CollapseEnvironment()

def parse_expression(expr):
    anchors = []
    parts = expr.strip().split("·")
    for part in parts:
        token = part.strip().strip("[]")
        if "^" not in token:
            raise ValueError(f"Invalid token format: {token}")
        symbol, alpha_str = token.split("^")
        symbol = symbol.strip()
        alpha = float(alpha_str.strip())
        index = symbol_to_index(symbol)
        anchors.append(Anchor(index=index, alpha=alpha))
    return anchors

def symbol_to_index(symbol):
    if symbol.isdigit():
        return int(symbol) % 60
    elif len(symbol) == 1 and symbol.isalpha():
        return (ord(symbol.upper()) - ord('A')) % 60
    else:
        raise ValueError(f"Unknown symbol: {symbol}")

def execute(filename):
    with open(filename, "r") as f:
        line = f.readline()
    anchors = parse_expression(line)
    print(f"📜 Parsed {len(anchors)} anchors.")
    return anchors
