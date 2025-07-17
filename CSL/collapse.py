# CSL/collapse.py

import os
import sys
from CSL.CollapseVM import CollapseVM
from CSL.CSLParser import CSLParser

try:
    from CSL.plotter import plot_trace
except ImportError:
    plot_trace = None

def main():
    vm = CollapseVM()
    parser = CSLParser()
    print("Collapse Symbolic Language (CSL) REPL. Type 'exit' to quit.")

    while True:
        try:
            line = input("CSL> ").strip()
        except EOFError:
            break

        if not line or line.lower() == "exit":
            break

        # Check for evolve command
        if line.startswith("evolve"):
            parts = line.split()
            if len(parts) == 3:
                try:
                    steps = int(parts[1])
                    filename = parts[2]
                    if not filename.endswith(".csv"):
                        print("[Error] Filename must end in .csv")
                        continue

                    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
                    os.makedirs(output_dir, exist_ok=True)
                    outpath = os.path.join(output_dir, filename)
                    vm.evolve(steps, outpath)

                    print(f"Ψ evolved {steps} steps.")
                    print(f"  γ[Ψ] = {vm.compute_gamma():.6f}")
                    print(f"  H[Ψ] = {vm.compute_entropy():.6f}")
                    print(f"  Collapse trace saved to: {outpath}")
                except Exception as e:
                    print(f"[Error] {e}")
            else:
                print("[Usage] evolve N filename.csv")
            continue

        # Check for plot command
        if line.startswith("plot"):
            parts = line.split()
            if len(parts) == 2:
                if plot_trace:
                    fname = parts[1]
                    full_path = os.path.join(os.path.dirname(__file__), "outputs", fname)
                    if not os.path.exists(full_path):
                        print(f"[Error] File not found: {full_path}")
                    else:
                        plot_trace(full_path)
                else:
                    print("[Error] Plotter module not available.")
            else:
                print("[Usage] plot filename.csv")
            continue

        try:
            stmt = parser.parse(line)
            if stmt is not None:
                output = vm.execute(stmt)
                if output is not None:
                    print(output)
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    main()
