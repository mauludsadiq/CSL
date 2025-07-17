import random

def apply_random_restriction(clauses, n, rho):
    restricted = []
    assigned = {}
    for var in range(1, n + 1):
        if random.random() > rho:
            assigned[var] = random.choice([True, False])
    for clause in clauses:
        new_clause = []
        for lit in clause:
            var = abs(lit)
            if var in assigned:
                val = assigned[var]
                if (lit > 0 and val) or (lit < 0 and not val):
                    new_clause = None  # Clause satisfied → drop
                    break
                # Otherwise, literal is false → skip
            else:
                new_clause.append(lit)
        if new_clause is not None and len(new_clause) > 0:
            restricted.append(new_clause)
    return restricted
