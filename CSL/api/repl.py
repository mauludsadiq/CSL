# api/repl.py

from CollapseVM import CollapseVM
import json

# Initialize the VM
vm = CollapseVM()
vm.init_field()

# Vercel-compatible handler
def handler(request):
    try:
        body = json.loads(request.body)
        stmt = body.get("stmt", "")

        # Parse input
        if "::" in stmt:
            parts = [s.strip() for s in stmt.split("::")]
            parsed_stmt = ("assign", parts[0], parts[1])
        elif "=>" in stmt:
            parsed_stmt = ("evolve_step",)
        elif stmt.strip() == "γ[Ψ]":
            parsed_stmt = ("gamma",)
        elif stmt.strip() == "H[Ψ]":
            parsed_stmt = ("entropy",)
        else:
            raise ValueError("Invalid input.")

        # Execute and respond
        result = vm.execute(parsed_stmt)
        return {
            "statusCode": 200,
            "body": json.dumps({ "output": result })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }
