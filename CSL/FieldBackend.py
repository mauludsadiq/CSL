# CSL/FieldBackend.py

import numpy as np

class F3Cube:
    def __init__(self):
        self.data = np.random.rand(3, 3, 3)
        self.data = self.data / np.linalg.norm(self.data)

    def __abs__(self):
        return np.abs(self.data)

    def __sub__(self, other):
        result = F3Cube()
        result.data = self.data - other
        return result

    def __isub__(self, other):
        self.data -= other
        return self

    def __truediv__(self, other):
        result = F3Cube()
        result.data = self.data / other
        return result

    def __itruediv__(self, other):
        self.data /= other
        return self

    def __neg__(self):
        result = F3Cube()
        result.data = -self.data
        return result

    def __mul__(self, other):
        result = F3Cube()
        result.data = self.data * other
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        result = F3Cube()
        result.data = self.data + other
        return result

    def __iadd__(self, other):
        self.data += other
        return self

    def __repr__(self):
        return f"F3Cube({self.data})"
