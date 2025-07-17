# collapse_vm/interpreter.py

from collapse_vm.collapse_script import parse_script, CollapseEnvironment
from collapse_vm.collapse_trace import trace_and_export

def execute_script(
    filename,
    mutate_prob=0.1,
    target=None,
    theme="default",
    output_format="gif",
    curve="linear",
    report=False
):
    anchors = parse_script(filename)
    env = CollapseEnvironment(mutate_prob=mutate_prob, curve=curve)
    collapse_index, expression = env.collapse(anchors)

    if report:
        trace_and_export(
            anchors=anchors,
            collapse_index=collapse_index,
            expression=expression,
            theme=theme,
            target=target,
            output_format=output_format
        )

    return collapse_index, expression
