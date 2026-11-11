import os

from flask import Flask, jsonify, request


app = Flask(__name__)

FEATURE_DESCONTO_PROMO = os.getenv("FEATURE_DESCONTO_PROMO", "false").lower() == "true"

@app.route("/")
def home():
    return jsonify({"mensagem": "Bem-vindo a API FastOrder!"}), 200


@app.route("/api/status")
def status():
    return jsonify({
        "status": "Operacional", 
        "Servico": "FastOrder",
        "flags": {
            "FEATURE_DESCONTO_PROMO": FEATURE_DESCONTO_PROMO
        }
        }), 200


@app.route("/api/soma", methods=["GET"])
def soma():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        resultado = a + b

        return jsonify({"resultado": resultado}), 200
    except (TypeError, ValueError):
        return jsonify({"erro": "Parâmetros inválidos"}), 400

# Nova Rota - Protegida por Feature Flag
@app.route("/api/desconto")
def desconto():
    if not FEATURE_DESCONTO_PROMO:
        return jsonify({"erro": "Funcionalidade em construcao ou desativada temporariamente.",
                        "flag_status": False}), 403
    try:
        valor_total = float(request.args.get('valor', 0))
        porcentagem = float(request.args.get('porcentagem', 10))

        if valor_total <= 0:
            return jsonify({"erro": "O valor total deve ser maior que zero."}), 400

        valor_com_desconto = valor_total - (valor_total * (porcentagem / 100))
        return jsonify({
            "Valor original": valor_total,
            "Desconto aplicado (%)": porcentagem,
            "Valor com desconto": valor_com_desconto
        })
    except (TypeError, ValueError):
        return jsonify({"erro": "Parametros de desconto invalidos"}), 400

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5000)
