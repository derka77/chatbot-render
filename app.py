from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import handle_user_query  # ✅ On utilise notre propre chatbot
import logging
import os
import logging
import traceback

# Configurer le logging pour capturer toutes les erreurs
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Erreur détectée : {e}")
    traceback_str = traceback.format_exc()
    logging.error(traceback_str)
    return "Internal Server Error", 500

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 🔹 Route d'accueil pour vérifier si le serveur tourne
@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!"

# 🔹 Route principale du chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    user_phone = request.json.get("phone_number")  # Récupérer le numéro de téléphone

    app.logger.info(f"📩 Message reçu : {user_message} de {user_phone}")
    bot_reply = handle_user_query(user_message, user_phone)
    
    app.logger.info(f"🤖 Bot répond : {bot_reply}")
    return jsonify({"response": bot_reply})

# 🔹 Route pour gérer WhatsApp via Twilio
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    user_phone = request.values.get('From', '').strip()

    app.logger.info(f"📩 Message brut reçu: {incoming_msg}")
    app.logger.info(f"📞 Numéro de l'utilisateur: {user_phone}")

    bot_reply = handle_user_query(incoming_msg, user_phone)
    
    app.logger.info(f"🤖 Réponse envoyée: {bot_reply}")
    
    # ✅ Répondre via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render définit un port automatiquement
    app.run(host="0.0.0.0", port=port, debug=True)
