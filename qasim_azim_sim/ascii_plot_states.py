import pandas as pd

# Load data
data = pd.read_csv('output/trajectory_data.csv')

def ascii_chart(series, label, width=50, height=10):
    min_val = series.min()
    max_val = series.max()
    scale = (max_val - min_val) / height

    print(f"\n{label} (min: {min_val:.2f}, max: {max_val:.2f})")
    for level in reversed(range(height+1)):
        threshold = min_val + level * scale
        line = ''
        for val in series:
            if val >= threshold:
                line += '#'
            else:
                line += ' '
        print(f"{threshold:7.2f} | {line}")

# Plot s_q and s_a
ascii_chart(data['s_q'], 's_q (Qasim state)')
ascii_chart(data['s_a'], 's_a (Azim state)')
