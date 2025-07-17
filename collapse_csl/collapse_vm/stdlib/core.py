# collapse_vm/stdlib/core/loop.py

from fractions import Fraction

def loop(exprs):
    """Process a list of expressions into the environment dict."""
    env = {}
    for anchor in exprs:
        key = anchor.index
        if key not in env:
            env[key] = 0
        env[key] += float(anchor.alpha)
    return env

def recursive_weighting(env, depth=3):
    """Apply recursive weighting to the environment."""
    def recurse(e, level):
        if level == 0:
            return e
        return {k: v * (1 + 1 / (level + 1)) for k, v in recurse(e, level - 1).items()}
    
    return recurse(env, depth)
