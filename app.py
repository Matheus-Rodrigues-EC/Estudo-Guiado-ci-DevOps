from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"mensagem": "Bem-vindo à API FastOrder!"}), 200


@app.route("/api/status")
def status():
    return jsonify({"status": "Operacional", "Serviço": "FastOrder"}), 200


@app.route("/api/soma", methods=["GET"])
def soma():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        resultado = a - b

        return jsonify({"resultado": resultado}), 200
    except (TypeError, ValueError):
        return jsonify({"erro": "Parâmetros inválidos"}), 400


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
