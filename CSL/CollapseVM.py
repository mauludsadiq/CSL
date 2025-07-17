# CSL/CollapseVM.py

import numpy as np
from .FieldBackend import F3Cube
import re
import csv

class CollapseVM:
    def __init__(self):
        self.Ψ = None
        self.alpha = 1.0
        self.lmbda = 0.1

    def init_field(self):
        self.Ψ = F3Cube()
        print("Initializing Ψ over group F3^3")

    def set_lagrangian(self, alpha, lmbda):
        self.alpha = alpha
        self.lmbda = lmbda
        print(f"Lagrangian set: α={alpha}, λ={lmbda}")

    def compute_entropy(self):
        if self.Ψ is None:
            raise ValueError("Ψ not initialized.")
        prob = np.abs(self.Ψ.data) ** 2
        prob = prob / prob.sum()
        return -np.sum(prob * np.log(prob + 1e-9))

    def compute_gamma(self):
        if self.Ψ is None:
            raise ValueError("Ψ not initialized.")
        return float(np.abs(np.sum(self.Ψ.data)) / np.linalg.norm(self.Ψ.data))

    def step(self):
        if self.Ψ is None:
            raise ValueError("Ψ not initialized.")
        grad = -self.alpha * self.Ψ.data + self.lmbda * np.random.normal(0, 0.1, self.Ψ.data.shape)
        self.Ψ.data -= grad
        self.Ψ.data = self.Ψ.data / np.linalg.norm(self.Ψ.data)

    def evolve(self, steps, trace_path=None):
        if self.Ψ is None:
            raise ValueError("Ψ not initialized.")
        trace = []

        for i in range(steps):
            self.step()
            γ = self.compute_gamma()
            H = self.compute_entropy()
            trace.append((i + 1, γ, H))

        if trace_path:
            with open(trace_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["step", "gamma", "entropy"])
                writer.writerows(trace)

    def execute(self, stmt):
        kind = stmt[0]

        if kind == "assign":
            lhs, rhs = stmt[1], stmt[2]
            if lhs == "Ψ" and rhs == "ψ[𝔽₃³]":
                self.init_field()
            elif lhs == "𝓛[Ψ]":
                match = re.match(r"([\d.]+)\*E\[Ψ\] \+ ([\d.]+)\*H\[Ψ\]", rhs)
                if match:
                    alpha = float(match.group(1))
                    lmbda = float(match.group(2))
                    self.set_lagrangian(alpha, lmbda)
                else:
                    raise ValueError("Unrecognized lagrangian form.")
            else:
                raise ValueError(f"Unknown assignment: {lhs} = {rhs}")

        elif kind == "evolve_step":
            self.step()
            return "Ψ evolved one step."

        elif kind == "gamma":
            return f"γ[Ψ] = {self.compute_gamma():.6f}"

        elif kind == "entropy":
            return f"H[Ψ] = {self.compute_entropy():.6f}"

        elif kind == "time":
            return "T↓[Ψ] = 1000 steps"

        return None
