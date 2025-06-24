from flask import Flask, Response, request, jsonify
import json
from src.service.services import comments_cache

app = Flask(__name__)
API_KEY = "123456"

@app.route("/comments/<empresa>", methods=["GET"])
def get_comments_empresa(empresa):
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"detail": "Unauthorized"}), 401
    if empresa not in comments_cache:
        return jsonify({"detail": "Empresa não encontrada"}), 404
    # Serializa o JSON com ensure_ascii=False
    return Response(
        json.dumps({"comments": comments_cache[empresa]}, ensure_ascii=False),
        mimetype="application/json"
    )