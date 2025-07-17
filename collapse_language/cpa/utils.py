# cpa/utils.py

import numpy as np
import pandas as pd

def export_expression_matrix(csv_path):
    data = np.load("data/vectors.npy", allow_pickle=True).item()
    df = pd.DataFrame.from_dict(data, orient="index")
    df.to_csv(csv_path)
    print(f"[✓] Exported expression matrix to {csv_path}")
