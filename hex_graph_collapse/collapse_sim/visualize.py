import matplotlib.pyplot as plt
import networkx as nx

def plot_validators(G, validators, title="Validator Field", filename=None):
    pos = {v: (v[1], -v[0]) for v in G.nodes()}
    vals = [validators[v] for v in G.nodes()]
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, node_color=vals, node_size=60, cmap=plt.cm.viridis)
    plt.title(title)
    plt.axis('off')
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.close()

def plot_entropy_curve(main, secondary, filename=None):
    plt.figure()
    plt.plot(range(len(main)), main, label="Main")
    plt.plot(range(len(secondary)), secondary, label="Secondary")
    plt.xlabel("Step")
    plt.ylabel("Entropy H")
    plt.title("Entropy Decay")
    plt.legend()
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.close()

def plot_anchor_trajectory(main, secondary, filename=None):
    main_x = [a[0] for a in main]
    main_y = [a[1] for a in main]
    sec_x = [a[0] for a in secondary]
    sec_y = [a[1] for a in secondary]

    plt.figure()
    plt.plot(main_x, main_y, 'o-', label="Main Ψ₃₃")
    plt.plot(sec_x, sec_y, 's--', label="Secondary Ψ₃₃")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Anchor Ψ₃₃ Trajectory")
    plt.legend()
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.close()

def plot_mode_projections(main_proj, sec_proj, filename=None):
    steps = len(main_proj)
    plt.figure(figsize=(8, 5))
    for j in range(len(main_proj[0])):
        main_vals = [row[j] for row in main_proj]
        sec_vals = [row[j] for row in sec_proj]
        plt.plot(range(steps), main_vals, label=f"Main mode {j}")
        plt.plot(range(steps), sec_vals, linestyle='--', label=f"Secondary mode {j}")
    plt.xlabel("Step")
    plt.ylabel("Projection Value")
    plt.title("Spectral Mode Projections")
    plt.legend()
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.close()
