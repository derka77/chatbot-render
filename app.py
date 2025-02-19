from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import handle_user_query  # ✅ On utilise notre propre chatbot

app = Flask(__name__)

# 🔹 Ajout de la route d'accueil pour tester si le serveur tourne bien
@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    user_phone = request.json.get("phone_number")  # Récupérer le numéro de téléphone

    # ✅ Utiliser notre propre chatbot
    bot_reply = handle_user_query(user_message, user_phone)

    return jsonify({"response": bot_reply})

# 🔗 Route pour gérer WhatsApp via Twilio
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    user_phone = request.values.get('From', '').strip()  # ✅ Récupérer le numéro de téléphone

    # ✅ Utiliser `handle_user_query()` avec le numéro de téléphone
    bot_reply = handle_user_query(incoming_msg, user_phone)

    # 🔍 Debug : afficher les logs des messages
    print(f"[DEBUG] Message brut reçu: {incoming_msg} de {user_phone}")
    print(f"[📤 RÉPONSE ENVOYÉE] {bot_reply}")

    # ✅ Répondre via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render définit un port automatiquement
    app.run(host="0.0.0.0", port=port, debug=True)


