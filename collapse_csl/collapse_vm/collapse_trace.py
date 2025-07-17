import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def trace_and_export(anchors, theme="default", report=False, output_format="gif", target=None):
    """
    Visualize and export the collapse trace from a list of anchor states.

    Parameters:
    - anchors: list of (index, alpha) tuples.
    - theme: Matplotlib theme (e.g., "default", "ggplot").
    - report: Whether to generate a CSV report of the collapse sequence.
    - output_format: "gif" or "mp4".
    - target: Optional float collapse target, used for visual annotation.
    """

    # Prepare dataframe
    df = pd.DataFrame(anchors, columns=["index", "alpha"])

    # Apply theme
    plt.style.use(theme)

    fig, ax = plt.subplots()
    scat = ax.scatter([], [], s=[], c=[], cmap='viridis', alpha=0.8)
    ax.set_xlim(-1, 60)
    ax.set_ylim(0, df["alpha"].max() * 1.2)

    if target:
        ax.axhline(target, color='red', linestyle='--', label=f"Target = {target}")
        ax.legend()

    def update(frame):
        current = df.iloc[:frame + 1]
        scat.set_offsets(list(zip(current["index"], current["alpha"])))
        scat.set_sizes(100 * current["alpha"])
        scat.set_array(current["index"])
        return scat,

    ani = animation.FuncAnimation(fig, update, frames=len(df), repeat=False)

    if output_format == "gif":
        ani.save("collapse_trace.gif", writer="pillow", fps=2)
        print("✅ Saved: collapse_trace.gif")
    elif output_format == "mp4":
        ani.save("collapse_trace.mp4", writer="ffmpeg", fps=2)
        print("✅ Saved: collapse_trace.mp4")
    else:
        print("⚠️ Unknown output format. Use 'gif' or 'mp4'.")

    # Save data
    if report:
        df.to_csv("collapse_trace_report.csv", index=False)
        print("📄 Saved: collapse_trace_report.csv")

    plt.close()
