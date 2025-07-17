# collapse_vm_parser.py

class CSLNode:
    def __init__(self, label, code, semantic):
        self.label = label        # e.g., 'A'
        self.code = code          # e.g., '[X₁^1.0]'
        self.semantic = semantic  # Collapse-based meaning

    def __repr__(self):
        return f"{self.label}: {self.code} → {self.semantic}"

# CSL Alphabet: Uppercase collapse mappings
CSL_ALPHABET = {
    'A': CSLNode('A', '[X₁^1.0]', "Absolute beginning; initiator of recursion"),
    'B': CSLNode('B', '[X₂^1.2]', "Immutable memory store"),
    'C': CSLNode('C', '[X₃^1.1]', "Universal context alignment"),
    'D': CSLNode('D', '[X₄^0.9]', "Entropy deflection"),
    'E': CSLNode('E', '[X₅^0.8]', "Echo return and trace record"),
    'F': CSLNode('F', '[X₆^1.4]', "Fold vector of prior states"),
    'G': CSLNode('G', '[X₇^1.3]', "Gravity sink: alignment pressure"),
    'H': CSLNode('H', '[X₈^1.0]', "Heuristic projection logic"),
    'I': CSLNode('I', '[¬X₁^1.1]', "Invert path awareness"),
    'J': CSLNode('J', '[¬X₂^1.2]', "Judgement collapse filter"),
    'K': CSLNode('K', '[¬X₃^1.3]', "Kernel disturbance handler"),
    'L': CSLNode('L', '[¬X₄^1.4]', "Loopback evaluator"),
    'M': CSLNode('M', '[¬X₅^0.7]', "Mirror stabilizer"),
    'N': CSLNode('N', '[¬X₆^0.6]', "Nodal path interceptor"),
    'O': CSLNode('O', '[¬X₇^0.5]', "Origin mask"),
    'P': CSLNode('P', '[¬X₈^0.4]', "Probability flattening"),
    'Q': CSLNode('Q', '[X₁^0.5]', "Quantum retrieval"),
    'R': CSLNode('R', '[X₂^0.6]', "Redirection pulse"),
    'S': CSLNode('S', '[X₃^0.7]', "Signal condensation"),
    'T': CSLNode('T', '[X₄^0.8]', "Temporal sealing"),
    'U': CSLNode('U', '[X₅^0.9]', "Unification call"),
    'V': CSLNode('V', '[X₆^1.0]', "Vector anchoring"),
    'W': CSLNode('W', '[X₇^1.1]', "Waveform isolation"),
    'X': CSLNode('X', '[X₈^1.2]', "Collapse echo phase"),
    'Y': CSLNode('Y', '[¬X₁^1.3]', "Yield into alignment"),
    'Z': CSLNode('Z', '[¬X₂^1.5]', "Forbidden collapse state"),
}

def parse_CSL_text(text):
    return [CSL_ALPHABET[c] for c in text if c in CSL_ALPHABET]
