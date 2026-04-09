# bot_deltachat.py
import requests
import os
from deltachat2 import events
from deltabot_cli import BotCli

# --- Configuración ---
# Tu API Key de DeepSeek. ¡No la compartas!
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Inicializamos el bot con un nombre
cli = BotCli("deepseek_deltabot")

# --- Aquí empieza la magia: El bot reacciona a los mensajes nuevos ---
@cli.on(events.NewMessage)
def on_new_message(bot, accid, event):
    """Esta función se ejecuta cada vez que alguien le escribe al bot."""
    msg = event.msg
    # Solo responde a mensajes de texto, no a imágenes u otros tipos
    if not msg.text:
        return

    user_message = msg.text
    print(f"Mensaje de {msg.from_contact.addr}: {user_message}")

    # --- Llamada a la API de DeepSeek ---
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # Aquí preparamos la conversación para DeepSeek
    data = {
        "model": "deepseek-chat", # El modelo gratuito y rápido
        "messages": [
            {"role": "system", "content": "Eres un asistente útil y conciso."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,  # Controla la longitud de la respuesta para ahorrar tokens
        "temperature": 0.7
    }

    try:
        # Enviamos la petición a DeepSeek
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()

        # Extraemos la respuesta de DeepSeek
        ai_response = response.json()["choices"][0]["message"]["content"]
        print(f"Respuesta de DeepSeek: {ai_response[:50]}...")

        # Enviamos la respuesta de vuelta al chat
        bot.rpc.misc_send_text_message(accid, msg.chat_id, ai_response)

    except Exception as e:
        error_msg = "Lo siento, tuve un problema al procesar tu mensaje."
        print(f"Error: {e}")
        bot.rpc.misc_send_text_message(accid, msg.chat_id, error_msg)

# --- Arrancamos el bot ---
if __name__ == "__main__":
    if not DEEPSEEK_API_KEY:
        print("Error: La variable de entorno DEEPSEEK_API_KEY no está configurada.")
    else:
        cli.start()