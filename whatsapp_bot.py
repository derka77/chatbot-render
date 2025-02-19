from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import handle_user_query  # ✅ Importe le bon chatbot

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    
    # ✅ Utiliser notre propre chatbot, et non OpenAI
    bot_reply = handle_user_query(user_message)

    return jsonify({"response": bot_reply})

# 🔗 Route pour gérer WhatsApp via Twilio
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()

    # ✅ Utiliser `handle_user_query()` pour répondre
    bot_reply = handle_user_query(incoming_msg)

    # 🔍 Debug : afficher les logs des messages
    print(f"[📩 MESSAGE REÇU] {incoming_msg}")
    print(f"[📤 RÉPONSE ENVOYÉE] {bot_reply}")

    # Répondre via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
