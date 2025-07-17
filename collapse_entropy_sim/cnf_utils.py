import random

def generate_random_3cnf(n_vars, clause_density):
    n_clauses = int(clause_density * n_vars)
    clauses = []
    for _ in range(n_clauses):
        clause = []
        while len(clause) < 3:
            var = random.randint(1, n_vars)
            lit = var if random.random() < 0.5 else -var
            if lit not in clause and -lit not in clause:
                clause.append(lit)
        clauses.append(clause)
    return clauses  # List of 3-literal clauses
