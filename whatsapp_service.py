import os
import requests

def send_whatsapp_message(to_phone_number, message_text):
    """
    Envia uma mensagem de texto simples via WhatsApp Cloud API.
    """
    phone_number_id = os.environ.get("PHONE_NUMBER_ID")
    whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

    if not phone_number_id or not whatsapp_token:
        print("[ERRO WHATSAPP] PHONE_NUMBER_ID ou WHATSAPP_TOKEN não configurados nas variáveis de ambiente.")
        return False

    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message_text
        }
    }

    try:
        print(f"[WHATSAPP OUT] Enviando mensagem para {to_phone_number}...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"[WHATSAPP SUCCESS] Mensagem enviada com sucesso para {to_phone_number}!")
            return True
        else:
            print(f"[WHATSAPP ERROR] Falha ao enviar! Código: {response.status_code}")
            print(f"[WHATSAPP ERROR DETALHES]: {response.text}")
            return False

    except Exception as e:
        print(f"[WHATSAPP EXCEPTION] Erro ao conectar com API do WhatsApp: {e}")
        return False
