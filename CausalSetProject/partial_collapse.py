import collections
import sys

def compute_depths(n_events, causal_relations):
    """
    Compute the depth (longest path from minimal elements) for each event.
    """
    successors = collections.defaultdict(list)
    predecessors = collections.defaultdict(list)
    for u, v in causal_relations:
        successors[u].append(v)
        predecessors[v].append(u)

    in_degree = [0] * n_events
    for v in range(n_events):
        in_degree[v] = len(predecessors[v])
    depth = [None] * n_events

    queue = collections.deque([i for i in range(n_events) if in_degree[i] == 0])
    for i in queue:
        depth[i] = 0

    while queue:
        u = queue.popleft()
        for v in successors[u]:
            pred_depths = [depth[p] for p in predecessors[v]]
            depth[v] = 1 + max(pred_depths)
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return depth

def group_by_depth(depth):
    groups = collections.defaultdict(list)
    for i, d in enumerate(depth):
        groups[d].append(i)
    return dict(sorted(groups.items()))

def build_quotient_relations(causal_relations, depth):
    quotient_edges = set()
    for u, v in causal_relations:
        du, dv = depth[u], depth[v]
        if du != dv:
            quotient_edges.add((du, dv))
    return sorted(quotient_edges)

def describe_partial_collapse(n_events, causal_relations):
    depth = compute_depths(n_events, causal_relations)
    depth_groups = group_by_depth(depth)
    quotient_edges = build_quotient_relations(causal_relations, depth)

    print(f"✅ Depth-Based Partial Collapse of Causal Set with {n_events} Events\n")

    print("📚 Events Grouped by Depth Level:")
    for d, events in depth_groups.items():
        print(f"  • Depth D{d}: {sorted(events)} ({len(events)} events)")

    print("\n📐 Quotient Causal Set Structure (Clusters D0, D1, ...):")
    clusters = sorted(depth_groups.keys())
    print(f"  Nodes (Clusters): D{', D'.join(map(str, clusters))}")
    if quotient_edges:
        print("  Edges Between Clusters (Quotient DAG):")
        for du, dv in quotient_edges:
            print(f"    D{du} → D{dv}")
    else:
        print("  No edges between clusters found (trivial order).")

    print("\n📝 Summary:")
    print(f"  • Reduced {n_events} events → {len(clusters)} clusters.")
    print(f"  • Depth range: D{min(clusters)} to D{max(clusters)}.")
    print(f"  • Quotient DAG has {len(quotient_edges)} edges, retaining partial causal order.")

if __name__ == "__main__":
    causal_relations = [
        (0, 5), (0, 8), (0, 9),
        (1, 6), (1, 7),
        (2, 7), (2, 10),
        (3, 8), (3, 11),
        (4, 9), (4, 12),

        (5, 13), (5, 14),
        (6, 14), (6, 15),
        (7, 15), (7, 16),
        (8, 16), (8, 17),
        (9, 17), (9, 18),
        (10, 18), (10, 19),
        (11, 19), (11, 20),
        (12, 20), (12, 21),

        (13, 22), (14, 23),
        (15, 24), (16, 25),
        (17, 26), (18, 27),
        (19, 28), (20, 29),
        (21, 30),

        (13, 24), (14, 25), (15, 26),
        (16, 27), (17, 28), (18, 29), (19, 30),

        (22, 31), (23, 32), (24, 33),
        (25, 34), (26, 35), (27, 36),
        (28, 37), (29, 38), (30, 39),

        (31, 40), (32, 41), (33, 42),
        (34, 43), (35, 44), (36, 45),
        (37, 46), (38, 47), (39, 48),
        (39, 49)
    ]
    n_events = 50

    with open("partial_collapse_output.txt", "w") as f:
        sys.stdout = f
        describe_partial_collapse(n_events, causal_relations)
        sys.stdout = sys.__stdout__

    print("✅ Analysis complete. See partial_collapse_output.txt in your project folder.")
