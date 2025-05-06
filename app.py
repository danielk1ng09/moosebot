from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)

# ---------------------------------------------
# 1. Diccionario de medios (PDFs, imágenes, etc)
# ---------------------------------------------
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
    "Responde con el número o palabra clave 😊"
)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    text_in = request.form.get("Body", "").lower()
    response = MessagingResponse()
    msg = response.message()

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
        msg.body("No entendí tu solicitud. Por favor responde con un número del 1 al 5 o la palabra clave del tema.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
