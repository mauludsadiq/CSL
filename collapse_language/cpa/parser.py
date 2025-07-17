import re

def parse_expression(expr):
    pattern = r'\[X_(\d+)\^([\d\.]+)\]'
    return [(int(k), float(t)) for k, t in re.findall(pattern, expr)]
