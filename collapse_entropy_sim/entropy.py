import random
import numpy as np

def generate_random_3cnf(n, num_clauses):
    formula = []
    for _ in range(num_clauses):
        clause = []
        vars_in_clause = random.sample(range(n), 3)
        for var in vars_in_clause:
            literal = var + 1  # 1-based indexing
            if random.random() < 0.5:
                literal *= -1
            clause.append(literal)
        formula.append(clause)
    return formula

def apply_random_restriction(formula, n, rho):
    # Fix (1 - rho)*n variables to random values
    num_fixed = int((1 - rho) * n)
    fixed_vars = set(random.sample(range(1, n + 1), num_fixed))
    assignment = {var: random.choice([True, False]) for var in fixed_vars}
    
    new_formula = []
    for clause in formula:
        keep_clause = True
        reduced_clause = []
        for lit in clause:
            var = abs(lit)
            sign = lit > 0
            if var in assignment:
                if assignment[var] == sign:
                    keep_clause = False  # clause satisfied → drop
                    break
                # else, literal is false → don't include
            else:
                reduced_clause.append(lit)
        if keep_clause:
            if reduced_clause:  # avoid empty clause
                new_formula.append(reduced_clause)
    return new_formula

def evaluate_formula(formula, assignment):
    for clause in formula:
        clause_satisfied = False
        for lit in clause:
            var = abs(lit)
            sign = lit > 0
            if assignment.get(var, False) == sign:
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

def estimate_entropy(formula, n, max_samples=10000):
    satisfying = 0
    for _ in range(max_samples):
        assignment = {i + 1: random.choice([True, False]) for i in range(n)}
        if evaluate_formula(formula, assignment):
            satisfying += 1
    p = satisfying / max_samples
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)
