from collapse_vm.collapse_trace import trace_and_export

# Sample anchor collapse simulation
anchors = [(i, 1.0 + 0.05 * i) for i in range(30)]

trace_and_export(
    anchors=anchors,
    theme="default",
    report=True,
    output_format="gif",
    target=3
)
