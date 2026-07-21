from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return "Servidor do WhatsApp + Gemini funcionando!"


@app.route("/webhook", methods=["GET"])
def verify():

    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge

    return "Token inválido", 403


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    print("Mensagem recebida:")
    print(data)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
