import pandas as pd
import matplotlib.pyplot as plt

# Load the simulation data
data = pd.read_csv('output/trajectory_data.csv')

# Plot s_q and s_a over time
plt.figure(figsize=(10, 6))
plt.plot(data['t'], data['s_q'], label='s_q (Qasim state)', color='blue')
plt.plot(data['t'], data['s_a'], label='s_a (Azim state)', color='red')

# Target lines
plt.axhline(y=100, color='blue', linestyle=':', label='Target s_q = 100')
plt.axhline(y=1, color='red', linestyle=':', label='Target s_a = 1')

# Labels and formatting
plt.xlabel('Time')
plt.ylabel('State Value')
plt.title('State Variables Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
