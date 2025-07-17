# collapse_vm/visualization.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def plot_collapse(df, theme='default', title='Collapse Trace'):
    if theme == 'ggplot':
        plt.style.use('ggplot')
    else:
        plt.style.use('default')

    fig, ax = plt.subplots()
    ax.plot(df['index'], df['power'], marker='o', linestyle='-')
    ax.set_title(title)
    ax.set_xlabel("Anchor Index")
    ax.set_ylabel("Power")
    plt.tight_layout()
    plt.show()


def animate_collapse(df, out_path='collapse_anim.mp4', theme='default', target=None):
    if theme == 'ggplot':
        plt.style.use('ggplot')
    else:
        plt.style.use('default')

    fig, ax = plt.subplots()
    ax.set_xlim(df['index'].min(), df['index'].max())
    ax.set_ylim(0, df['power'].max() * 1.1)
    ax.set_xlabel("Anchor Index")
    ax.set_ylabel("Power")
    ax.set_title("Collapse Animation")

    line, = ax.plot([], [], lw=2, color='blue', marker='o')
    target_line = None

    if target is not None:
        target_line = ax.axvline(x=target, color='red', linestyle='--', label='Collapse Target')
        ax.legend()

    def init():
        line.set_data([], [])
        return (line,)

    def update(frame):
        x = df['index'][:frame + 1]
        y = df['power'][:frame + 1]
        line.set_data(x, y)
        return (line,)

    ani = animation.FuncAnimation(
        fig, update, frames=len(df), init_func=init,
        blit=True, interval=200, repeat=False
    )

    ext = os.path.splitext(out_path)[1].lower()

    if ext == '.gif':
        ani.save(out_path, writer='pillow', fps=10)
    elif ext == '.mp4':
        ani.save(out_path, fps=10, extra_args=['-vcodec', 'libx264'])
    else:
        raise ValueError("Unsupported format. Use .mp4 or .gif")

    plt.close()
