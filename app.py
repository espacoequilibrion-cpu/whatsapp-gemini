import os
from flask import Flask, request, jsonify
from config import VERIFY_TOKEN
from gemini_service import get_gemini_response
from whatsapp_service import send_whatsapp_message

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Servidor do Espaço EquilibriON está online!", 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Rota de validação que a Meta chama ao clicar em 'Verificar e Salvar'.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"[WEBHOOK GET] Recebido - Mode: {mode} | Token: {token} | Challenge: {challenge}")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("[WEBHOOK GET] Verificação bem-sucedida!")
            # A Meta exige que retorne OBRIGATORIAMENTE o challenge como texto puro e status 200
            return str(challenge), 200
        else:
            print("[WEBHOOK GET] Token incorreto!")
            return "Token de verificação inválido", 403
            
    return "Rota do Webhook - Espaço EquilibriON", 200

@app.route('/webhook', methods=['POST'])
def receive_message():
    """
    Rota que recebe as mensagens do WhatsApp.
    """
    body = request.get_json()

    try:
        if body and body.get("object") == "whatsapp_business_account":
            entry = body.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if messages:
                message = messages[0]
                sender_phone = message.get("from")
                
                if message.get("type") == "text":
                    message_text = message.get("text", {}).get("body")
                    print(f"[WHATSAPP] Mensagem de {sender_phone}: {message_text}")
                    
                    resposta_ia = get_gemini_response(sender_phone, message_text)
                    send_whatsapp_message(sender_phone, resposta_ia)
                    
    except Exception as e:
        print(f"[ERRO POST]: {e}")

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
