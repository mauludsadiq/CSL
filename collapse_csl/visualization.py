import matplotlib.pyplot as plt
import pandas as pd

def plot_collapse(df, theme='default', title='Collapse Trace'):
    if theme == 'ggplot':
        plt.style.use('ggplot')
    elif theme == 'dark':
        plt.style.use('dark_background')
    else:
        plt.style.use('default')

    fig, ax = plt.subplots(figsize=(10, 6))

    for index, row in df.iterrows():
        anchor_str = f"X[{row['index']}]"
        ax.scatter(row['step'], row['index'], s=80 * row['alpha'], label=anchor_str)

    ax.set_xlabel('Step')
    ax.set_ylabel('Anchor Index')
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    plt.show()
