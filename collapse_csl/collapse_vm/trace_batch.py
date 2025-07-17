# collapse_vm/trace_batch.py

import pandas as pd

def batch_trace(env, target=None):
    """Batch trace environment into a pandas DataFrame for reporting."""
    rows = []
    for k, v in env.items():
        rows.append({
            "AnchorIndex": k,
            "Weight": v,
            "Delta": abs(k - target) if target is not None else None
        })
    return pd.DataFrame(rows)
