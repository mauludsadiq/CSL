import os
from collapse_sim.graph_utils import create_hex_graph, compute_laplacian_modes
from collapse_sim.collapse import initialize_validators
from collapse_sim.dynamics import (
    collapse_step, compute_entropy, project_modes
)
from collapse_sim.anchors import find_anchor
from collapse_sim.visualize import (
    plot_validators,
    plot_entropy_curve,
    plot_anchor_trajectory,
    plot_mode_projections
)
import pandas as pd

def main():
    os.makedirs("output", exist_ok=True)

    # Parameters
    steps = 10
    alpha = 1.0
    k = 30
    mode_count = 5

    # Graph + spectrum
    G = create_hex_graph(5, 5)
    node_index = {v: i for i, v in enumerate(G.nodes())}
    lambda_j, phi = compute_laplacian_modes(G, k=k)
    lambda_scaled = alpha * lambda_j

    # Initial validator fields
    validators_main = initialize_validators(G, constant=True)
    validators_secondary = initialize_validators(G, constant=False)

    # Tracking
    entropy_main, entropy_secondary = [], []
    anchors_main, anchors_secondary = [], []
    projections_main, projections_secondary = [], []
    validator_matrix_main, validator_matrix_secondary = [], []

    for step in range(steps):
        validators_main = collapse_step(validators_main, phi, lambda_scaled, G, node_index)
        validators_secondary = collapse_step(validators_secondary, phi, lambda_scaled, G, node_index)

        norm_main = normalize(validators_main)
        norm_secondary = normalize(validators_secondary)

        validator_matrix_main.append(norm_main)
        validator_matrix_secondary.append(norm_secondary)

        entropy_main.append(compute_entropy(validators_main))
        entropy_secondary.append(compute_entropy(validators_secondary))

        anchors_main.append(find_anchor(phi, 0, G, node_index))
        anchors_secondary.append(find_anchor(phi, 0, G, node_index))

        projections_main.append(project_modes(norm_main, phi, mode_count))
        projections_secondary.append(project_modes(norm_secondary, phi, mode_count))

    # Save data
    pd.DataFrame({
        "step": list(range(steps)),
        "entropy_main": entropy_main,
        "entropy_secondary": entropy_secondary
    }).to_csv("output/entropy.csv", index=False)

    pd.DataFrame({
        "step": list(range(steps)),
        "anchor_main_x": [a[0] for a in anchors_main],
        "anchor_main_y": [a[1] for a in anchors_main],
        "anchor_secondary_x": [a[0] for a in anchors_secondary],
        "anchor_secondary_y": [a[1] for a in anchors_secondary]
    }).to_csv("output/anchor_trajectory.csv", index=False)

    pd.DataFrame(projections_main, columns=[f"mode_{i}" for i in range(mode_count)]).to_csv("output/projection_main.csv", index=False)
    pd.DataFrame(projections_secondary, columns=[f"mode_{i}" for i in range(mode_count)]).to_csv("output/projection_secondary.csv", index=False)

    pd.DataFrame(validator_matrix_main, columns=[str(v) for v in G.nodes()]).to_csv("output/validators_main.csv", index=False)
    pd.DataFrame(validator_matrix_secondary, columns=[str(v) for v in G.nodes()]).to_csv("output/validators_secondary.csv", index=False)

    # Plot results
    plot_entropy_curve(entropy_main, entropy_secondary, filename="output/entropy_curve.png")
    plot_anchor_trajectory(anchors_main, anchors_secondary, filename="output/anchor_trajectory.png")
    plot_mode_projections(projections_main, projections_secondary, filename="output/mode_projections.png")

def normalize(validators):
    total = sum(validators.values())
    return [validators[v] / total for v in validators]

if __name__ == "__main__":
    main()
