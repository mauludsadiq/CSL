# CSL/CSLParser.py

class CSLParser:
    def parse(self, line):
        line = line.strip()

        if "::" in line:
            lhs, rhs = map(str.strip, line.split("::", 1))
            return ("assign", lhs, rhs)

        if "=>" in line:
            lhs, rhs = map(str.strip, line.split("=>", 1))
            return ("evolve_step", lhs, rhs)

        if line.startswith("γ[") and line.endswith("]"):
            return ("gamma", line)

        if line.startswith("H[") and line.endswith("]"):
            return ("entropy", line)

        if line.startswith("T↓[") and line.endswith("]"):
            return ("time", line)

        return None
