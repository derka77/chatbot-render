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
    
    if user_input.startswith("salam"):
        return "wa aleykoum salam, how can I help?"
    
    # ✅ Gestion des questions détectées
    if "battery" in user_input or "drain" in user_input:
        return "The battery life is great, lasts several hours without any issue."
    elif "scratches" in user_input or "broken screen" in user_input:
        return "No scratches, no damage. The screen is in perfect condition."
    elif "box" in user_input or "charger" in user_input:
        return "Yes, it comes with the original box and charger."
    elif "why you sell" in user_input or "reason" in user_input:
        return "I just don’t use it much, so I decided to sell."
    elif "original" in user_input or "copy" in user_input:
        return "It’s the original Apple MacBook Pro."
    elif "deliver" in user_input or "near me" in user_input:
        return "I prefer to meet in person so you can check the laptop first."
    elif "how old" in user_input or "year" in user_input:
        return "It was bought in 2023, so it’s still quite new."
    elif "test before buy" in user_input or "try" in user_input:
        return "Yes, of course. If you're interested, you can check it during the visit."
    elif "pictures" in user_input or "photos" in user_input:
        return f"Sure! Here’s a picture: {image_url}"
    elif "final price" in user_input or "last price" in user_input:
        return f"I was looking for {price} QAR, but I might adjust a little. What’s your best offer?"

    # 🔹 Gestion des visites et négociation du prix
    for handler in [lambda inp: handle_visit_request(inp, user_phone), lambda inp: handle_price_negotiation(inp, user_phone)]:
        response = handler(user_input)
        if response:
            return response

    return random.choice(RESPONSE_VARIANTS)

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
