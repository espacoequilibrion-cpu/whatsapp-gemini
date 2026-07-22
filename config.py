import os

# Credenciais do WhatsApp (Meta)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "equilibrion123")
WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

# Credenciais do Gemini (Google)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Modelo de IA sugerido (o 1.5 Flash é o mais rápido e eficiente para chats de WhatsApp)
GEMINI_MODEL = "gemini-1.5-flash"
