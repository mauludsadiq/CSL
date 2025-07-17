import pandas as pd
import plotly.graph_objects as go
import os

def plot_anchor_path_3d(anchor_csv_path, save=False, filename="output/anchor_path_3d.png"):
    """
    Plots the 3D trajectory of the collapse anchor (Ψ₃₃) over time.

    Parameters:
        anchor_csv_path (str): Path to CSV file containing x, y, z columns.
        save (bool): Whether to save the image to disk.
        filename (str): Path to save image (used only if save=True).
    """
    # Check that file exists
    if not os.path.exists(anchor_csv_path):
        raise FileNotFoundError(f"CSV file not found: {anchor_csv_path}")

    # Load anchor trajectory
    df = pd.read_csv(anchor_csv_path)
    if not {"x", "y", "z"}.issubset(df.columns):
        raise ValueError("CSV must contain 'x', 'y', and 'z' columns.")

    x, y, z = df["x"], df["y"], df["z"]

    # Build 3D plot
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x, y=y, z=z,
                mode="lines+markers",
                marker=dict(size=5, color=z, colorscale='Viridis', opacity=0.8),
                line=dict(color="royalblue", width=4)
            )
        ]
    )

    fig.update_layout(
        title="Ψ₃₃ Anchor Trajectory in 3D Collapse Field",
        scene=dict(
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
            zaxis_title="Collapse Depth (Z)",
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=700
    )

    if save:
        # Ensure output folder exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fig.write_image(filename)
    else:
        fig.show()
