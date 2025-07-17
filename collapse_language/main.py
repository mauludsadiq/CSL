from expressions import expression_list
from cpa.simulator import simulate_expression

if __name__ == "__main__":
    for i, expr in enumerate(expression_list, 1):
        final_state, trajectory, roles = simulate_expression(expr)
        print(f"\n--- Expression E{i} ---")
        print(f"Expr: {expr}")
        print(f"Final State: {final_state}")
        print("Roles:")
        for role, t in roles:
            print(f"  {role} (t={t})")
