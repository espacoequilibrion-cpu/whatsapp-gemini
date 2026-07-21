from flask import Flask, request
import google.generativeai as genai
import requests
import os

app = Flask(__name__)

# ================================
# CONFIGURAÇÕES
# ================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-pro")

SYSTEM_PROMPT = """
Você é o assistente virtual do Espaço EquilibriON.

Sempre responda de forma cordial.

Nunca invente informações.

Caso não saiba responder alguma pergunta,
informe que irá encaminhar para nossa equipe.

Informações da clínica:

- Avaliação presencial ou online: R$300.
- Sessões de reabilitação: R$300.
- Especialidade em reabilitação neurológica.
- Trabalhamos com lesão medular, AVC, Parkinson,
Esclerose Múltipla e outras doenças neurológicas.

Sempre tente finalizar perguntando
como pode ajudar ou oferecendo agendamento.
"""# ================================
# VERIFICAÇÃO DO WEBHOOK DA META
# ================================

@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Erro de verificação", 403


# ================================
# ENVIA MENSAGEM AO WHATSAPP
# ================================

def enviar_mensagem(numero, mensagem):

    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }

    requests.post(url, headers=headers, json=body)# ================================
# RECEBE MENSAGEM DO WHATSAPP
# ================================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:

        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return "ok", 200

        mensagem = value["messages"][0]["text"]["body"]
        numero = value["messages"][0]["from"]

        print(f"Mensagem recebida: {mensagem}")

        resposta = model.generate_content(
            SYSTEM_PROMPT + "\n\nPaciente: " + mensagem
        )

        texto = resposta.text

        enviar_mensagem(numero, texto)

    except Exception as erro:

        print("ERRO:", erro)

    return "ok", 200


# ================================
# INICIAR SERVIDOR
# ================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
