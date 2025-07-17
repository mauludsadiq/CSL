from collapse_vm.io_interface import Anchor
import random

def loop(anchors):
    total = sum(a.index * float(a.alpha) for a in anchors)
    collapsed_index = int(total) % 60
    return Anchor(collapsed_index, 1.0)

def recursive_weighting(anchors, w):
    return [Anchor(a.index, float(a.alpha) * w) for a in anchors]
