import re

# Pattern matches [X^n.n]
VALID_PATTERN = re.compile(r'\[\s?[A-Z]\^\d+\.\d+\s?\]')

def validate_cgs(csl_input: str) -> bool:
    tokens = re.findall(VALID_PATTERN, csl_input)
    return len(tokens) > 0 and all(VALID_PATTERN.fullmatch(t.strip()) for t in csl_input.split())
