# api/repl.py

from CSL.CollapseVM import CollapseVM
import json

vm = CollapseVM()
vm.init_field()

def handler(request):  # Vercel Python expects this signature
    try:
        body = json.loads(request.body.decode())  # decode bytes
        stmt = body.get("stmt", "")

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
