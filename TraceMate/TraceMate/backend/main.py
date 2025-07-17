from flask import Flask, request, jsonify, make_response
import chess
from validator_engine import select_best_move_from_curvature

app = Flask(__name__)

@app.route("/best-move", methods=["POST", "OPTIONS"])
def best_move():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response, 200

    try:
        data = request.get_json()
        fen = data.get("fen", "")
        board = chess.Board(fen)
        
        result = select_best_move_from_curvature(board)

        response = jsonify({
            "best_move": result["best_move"].uci(),
            "archetype": result["archetype"],
            "score": result["score"]
        })
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response, 200
    except Exception as e:
        response = jsonify({ "error": str(e) })
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
