import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model, location_map_url
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ajoute le dossier courant au chemin des imports
from config import FORBIDDEN_WORDS, RESPONSE_VARIANTS, FOLLOW_UP_VARIANTS
from rapidfuzz import process, fuzz
import openai  # Import OpenAI API
import os
from dotenv import load_dotenv
load_dotenv()  # Charge les variables d'environnement du fichier .env

# 🔹 Configure ta clé API OpenAI (Stocke-la en variable d’environnement)
openai.api_key = os.getenv("OPENAI_API_KEY")  


# Historique des échanges
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}
buyer_attempts = {}

# Configuration de Twilio
twilio_client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

# Fonction pour nettoyer les mots interdits
def clean_text(text):
    for word, replacement in FORBIDDEN_WORDS.items():
        text = text.replace(word, replacement)
    return text

# Fonction pour enregistrer les conversations pour statistiques
def save_conversation(user_phone, message):
    user_conversations.setdefault(user_phone, []).append(message)

# Fonction pour convertir une offre de prix en entier
def convert_price_format(price_str):
    price_str = price_str.lower().replace("qar", "").replace(",", "").strip()
    match = re.search(r'\b\d+\b', price_str)
    if match:
        return int(match.group(0))
    return None

# Gestion de la négociation de prix
def handle_price_negotiation(user_input, user_phone):
    offer = convert_price_format(user_input)
    if offer is not None:
        save_conversation(user_phone, f"Offer detected: {offer} QAR")
        if offer >= min_price:
            return clean_text(f"Alright, {offer} QAR sounds fair. Let's proceed.")
        else:
            return clean_text(f"I was looking for {price} QAR, but I might adjust a little. What’s your best offer?")
    return clean_text(f"I was hoping for {price} QAR, let me know what you have in mind.")

# Proposer des créneaux de visite
def propose_appointment_slots():
    slots_text = "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots])
    return clean_text(f"If you're really interested, I can be available:\n{slots_text}\nThe price is {price} QAR, let me know what works for you.")

# Vérification des demandes de visite
def handle_visit_request(user_input, user_phone):
    visit_keywords = ["can i visit", "can i check", "see it", "meet to view"]
    if any(request in user_input for request in visit_keywords):
        return clean_text("Are you really interested? Let me know and we can arrange something.")
    return None

# Envoi des coordonnées et slots uniquement à l'acheteur
def send_details_to_buyer(user_phone):
    details = clean_text(
        f"I'm in {location}, Doha. Let me know if you want to check it out.\n"
        f"Available slots:\n" + "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots]) + "\n"
        f"Once confirmed, I will share the exact location and contact details."
    )
    twilio_client.messages.create(body=details, from_="+7470278321", to=user_phone)
    return "Check your messages for details."

# Envoi d'un résumé complet au vendeur
def send_summary_to_seller(user_phone, user_name):
    conversation_summary = " ".join(user_conversations[user_phone][-5:])
    summary = clean_text(
        f"Buyer {user_name}\n"
        f"Recent messages: {conversation_summary}\n"
        f"Buyer contact: {user_phone}\n"
        f"Available slots:\n" + "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots])
    )
    twilio_client.messages.create(body=summary, from_="+97470278321", to=seller_contact)
    return "Info sent to the seller."

# Gestion de la conversation principale
def handle_user_query(user_input, user_phone, user_name=""):
    user_input = unidecode.unidecode(user_input.strip().lower())
    save_conversation(user_phone, user_input)

    # 🔹 Envoi du message à GPT-4o
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful AI chatbot assisting buyers and sellers in a marketplace. Keep responses short and natural, without punctuation."},
                {"role": "user", "content": user_input}
            ]
        )
        gpt_response = response["choices"][0]["message"]["content"].strip()
        return gpt_response
    
    except Exception as e:
        print(f"Erreur OpenAI : {e}")
        return "Sorry something went wrong try again later"

# Test du chatbot
if __name__ == "__main__":
    test_phone = "+97412345678"
    test_name = "Ali"
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        bot_response = handle_user_query(user_message, test_phone, test_name)
        print(f"Chatbot: {bot_response}")
