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
    Rota obrigatória para a Meta verificar o webhook.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verificado com sucesso pela Meta!")
            return challenge, 200
        else:
            return "Token de verificação inválido", 403
            
    return "Página de verificação do Webhook", 200

@app.route('/webhook', methods=['POST'])
def receive_message():
    """
    Rota que recebe as mensagens dos pacientes.
    """
    body = request.get_json()

    try:
        # Verifica se o formato de dados é do WhatsApp (evita erros com mensagens de sistema)
        if body.get("object") == "whatsapp_business_account":
            entry = body.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            # Se realmente houver uma mensagem nova...
            if messages:
                message = messages[0]
                sender_phone = message.get("from") # Número do paciente
                
                # Só processamos mensagens de texto neste momento
                if message.get("type") == "text":
                    message_text = message.get("text", {}).get("body")
                    print(f"Nova mensagem de {sender_phone}: {message_text}")
                    
                    # 1. Pede para a IA pensar na resposta
                    resposta_ia = get_gemini_response(sender_phone, message_text)
                    
                    # 2. Envia a resposta de volta pelo WhatsApp
                    send_whatsapp_message(sender_phone, resposta_ia)
                    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

    # A Meta exige que a gente sempre responda "200 OK" rápido, senão ela fica tentando reenviar a mensagem.
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
