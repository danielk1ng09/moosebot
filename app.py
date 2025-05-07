from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
import re

app = Flask(__name__)

# Configura la API key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Historial por número
conversation_history = {}

# Diccionario de medios
DOCS = {
    "ficha": "https://drive.google.com/uc?export=download&id=1solJcjqA-4W6ux9GnQTl27CdXuRVKmGM",
    "fotos": "https://drive.google.com/uc?export=download&id=1TyWUkoDYYZruwJ5nsDu6zpKFHVWUjfvH",
    "comparativo": "https://drive.google.com/uc?export=download&id=1QbMT2YWuS2GlEAtPFe-onpup_O1M76uz",
    "video_demo": "https://drive.google.com/uc?export=download&id=13Du5G7ScQVLXEBBG0-Gei79IMxi9m8_j",
    "video_martillo": "https://drive.google.com/uc?export=download&id=13EIcD03XngdY17Y3mH6ORqHbd4VoOVqJ",
    "credito": "https://drive.google.com/uc?export=download&id=1ljIDDiTHh1O3hbkC9f4O5yAjNsS5KIb1",
    "contacto": "https://drive.google.com/uc?export=download&id=1AdbtjNAIgGOoIFlvccGPvRh4uflDLS04"
}

WELCOME_MSG = (
    "👋 ¡Hola! Soy Daniel, asesor de Moose México.\n"
    "🚜 *Retroexcavadora MS308 2025 – Motor Cummins 110 HP*\n"
    "💵 Precio: $1,400,000 MXN (IVA incluido)\n"
    "🚚 Envíos a todo México · 📦 Entrega inmediata\n\n"
    "¿Qué te interesa conocer?\n"
    "1️⃣ Ficha técnica\n"
    "2️⃣ Fotos & video\n"
    "3️⃣ Financiamiento\n"
    "4️⃣ Garantías\n"
    "5️⃣ Comparativo con Cat\n\n"
    "O puedes hacerme cualquier pregunta 😊"
)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    user_number = request.form.get("From", "")
    text_in = request.form.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    # Inicializa historial si no existe
    if user_number not in conversation_history:
        conversation_history[user_number] = []

    # Bienvenida
    if text_in in ("hola", "hi", "buenas"):
        msg.body(WELCOME_MSG)
        return str(response)

    # Mapeo de opciones
    if "1" in text_in or "ficha" in text_in:
        msg.body("Aquí tienes la ficha técnica:")
        msg.media(DOCS["ficha"])
    elif "2" in text_in or "foto" in text_in or "video" in text_in:
        msg.body("Te comparto el archivo con fotos:")
        msg.media(DOCS["fotos"])
    elif "3" in text_in or "financia" in text_in or "crédito" in text_in:
        msg.body("Este es nuestro plan de financiamiento:")
        msg.media(DOCS["credito"])
    elif "4" in text_in or "garantía" in text_in:
        msg.body("Nuestra garantía incluye:\n✅ 1 año o 1800 hrs con Moose\n✅ 2 años motor Cummins\n✅ Asesoría técnica incluida")
    elif "5" in text_in or "comparativo" in text_in or "cat" in text_in:
        msg.body("Aquí tienes el comparativo Moose vs Cat:")
        msg.media(DOCS["comparativo"])
    elif "martillo" in text_in:
        msg.body("Este es el video del martillo hidráulico:")
        msg.media(DOCS["video_martillo"])
    elif re.search(r"\d{2,4}\s?km", text_in):
        km = int(re.search(r"(\d{2,4})", text_in).group(1))
        extra_km = max(km - 600, 0)
        cost = extra_km * 125
        msg.body(f"La ruta es de {km} km. Cubrimos 600 km gratis.\nExcedente: {extra_km} km × $125 = ${cost:,.0f} MXN + IVA.")
    else:
        # Respuesta generada por OpenAI
        conversation_history[user_number].append({"role": "user", "content": text_in})
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation_history[user_number],
                max_tokens=500
            )
            reply = completion.choices[0].message["content"]
            conversation_history[user_number].append({"role": "assistant", "content": reply})
            msg.body(reply)
        except Exception as e:
            msg.body("Ocurrió un error al generar la respuesta. Por favor intenta más tarde.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
