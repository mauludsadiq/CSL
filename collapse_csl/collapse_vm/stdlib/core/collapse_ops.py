from collapse_vm.io_interface import Anchor

def loop(anchors):
    total = sum(a.index * float(a.alpha) for a in anchors)
    collapsed_index = int(total) % 60
    return Anchor(collapsed_index, 1.0)

def recursive_weighting(anchors, weight):
    return [Anchor(a.index, float(a.alpha) * weight) for a in anchors]

