# collapse_vm/report_gen.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report(df, theme='default'):
    """Generate a trace report CSV and plot visualization."""
    os.makedirs("trace_reports", exist_ok=True)
    csv_path = os.path.join("trace_reports", "trace_output.csv")
    df.to_csv(csv_path, index=False)
    
    if theme:
        plt.style.use(theme)

    fig, ax = plt.subplots()
    df_sorted = df.sort_values("AnchorIndex")
    ax.bar(df_sorted["AnchorIndex"], df_sorted["Weight"])
    ax.set_title("Collapse Trace Weights")
    ax.set_xlabel("Anchor Index")
    ax.set_ylabel("Weight")
    fig.tight_layout()

    plot_path = os.path.join("trace_reports", "trace_plot.png")
    fig.savefig(plot_path)
    plt.close()
