import requests
import json
from config import WHATSAPP_API_URL, WHATSAPP_TOKEN

def send_whatsapp_message(to_number, message_text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Estrutura obrigatória exigida pela Meta para enviar mensagens de texto
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_text
        }
    }
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Verifica se houve erro na requisição HTTP
        print(f"Mensagem enviada com sucesso para {to_number}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem no WhatsApp: {e}")
        if response is not None:
            print(f"Detalhes do erro Meta: {response.text}")
        return False
