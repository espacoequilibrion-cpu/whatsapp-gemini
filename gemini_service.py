import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import ESPACO_EQUILIBRION_PROMPT

# Configura a chave de API do Google
genai.configure(api_key=GEMINI_API_KEY)

# Dicionário para guardar a memória da conversa de cada paciente (pelo número do WhatsApp)
user_sessions = {}

def get_gemini_response(user_phone, user_message):
    try:
        # Se for a primeira vez que a pessoa manda mensagem, criamos um novo chat para ela
        if user_phone not in user_sessions:
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                system_instruction=ESPACO_EQUILIBRION_PROMPT
            )
            # Inicia um chat vazio que guardará o histórico automaticamente
            user_sessions[user_phone] = model.start_chat(history=[])
        
        # Pega a sessão (histórico) deste paciente
        chat_session = user_sessions[user_phone]
        
        # Envia a mensagem do paciente para o Gemini
        response = chat_session.send_message(user_message)
        
        return response.text
        
    except Exception as e:
        print(f"Erro no Gemini: {e}")
        return "Desculpe, estou passando por uma instabilidade no momento. Por favor, aguarde um instante e tente novamente, ou aguarde nossa secretária."
