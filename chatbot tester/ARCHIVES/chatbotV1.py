import openai
import os
import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model, location_map_url
from config import FORBIDDEN_WORDS, RESPONSE_VARIANTS, FOLLOW_UP_VARIANTS
from rapidfuzz import process, fuzz
from openai import OpenAI

# Initialisation du client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Historique des échanges
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}
buyer_attempts = {}

# Configuration de Twilio
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

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

# 🔥 Gestion des questions spécifiques sur le produit
def handle_product_questions(user_input):
    user_input = user_input.lower()

    if "model" in user_input:
        return f"It's a {title}, category: {category}."
    if "year" in user_input:
        return f"The model year is {year_model}."
    if "battery" in user_input:
        return "The battery life is great, lasts several hours without any issue."
    if "condition" in user_input or "scratch" in user_input:
        return f"It's in {condition} condition, no issues."
    if "box" in user_input or "charger" in user_input:
        return "Yes, it comes with the original box and charger."
    if "test" in user_input:
        return "Yes, you can test it before buying."

    return None

# 🔥 Gestion de la négociation de prix
def handle_price_negotiation(user_input, user_phone):
    offer = convert_price_format(user_input)
    if offer is not None:
        save_conversation(user_phone, f"Offer detected: {offer} QAR")
        if offer >= min_price:
            return clean_text(f"Alright, {offer} QAR sounds fair. Let's proceed.")
        else:
            return clean_text(f"I was looking for {price} QAR, but I might adjust a little. What’s your best offer?")
    
    return None  # Ne renvoie rien si ce n'est pas une négociation de prix

# 🔥 Proposer des créneaux de visite
def propose_appointment_slots():
    slots_text = "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots])
    return clean_text(f"If you're really interested, I can be available:\n{slots_text}\nThe price is {price} QAR, let me know what works for you.")

# 🔥 Vérification des demandes de visite
def handle_visit_request(user_input):
    visit_keywords = ["can i visit", "can i check", "see it", "meet to view"]
    if any(request in user_input for request in visit_keywords):
        return clean_text("Are you really interested? Let me know and we can arrange something.")
    return None

# 🔥 Envoi des coordonnées et slots uniquement à l'acheteur
def send_details_to_buyer(user_phone):
    details = clean_text(
        f"I'm in {location}, Doha. Let me know if you want to check it out.\n"
        f"Available slots:\n" + "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots]) + "\n"
        f"Once confirmed, I will share the exact location and contact details."
    )
    twilio_client.messages.create(body=details, from_="+7470278321", to=user_phone)
    return "Check your messages for details."

# 🔥 Envoi d'un résumé complet au vendeur
def send_summary_to_seller(user_phone, user_name):
    conversation_summary = " ".join(user_conversations.get(user_phone, [])[-5:])
    summary = clean_text(
        f"Buyer {user_name}\n"
        f"Recent messages: {conversation_summary}\n"
        f"Buyer contact: {user_phone}\n"
        f"Available slots:\n" + "\n".join([f"- {slot.replace('-', ' between ')}" for slot in available_slots])
    )
    twilio_client.messages.create(body=summary, from_="+97470278321", to=seller_contact)
    return "Info sent to the seller."

# 🔥 Gestion de la conversation principale
def handle_user_query(user_input, user_phone, user_name=""):
    user_input = unidecode.unidecode(user_input.strip().lower())
    save_conversation(user_phone, user_input)

    # 🔹 Salam → Réponse spécifique
    if user_input.startswith("salam"):
        return "wa aleykoum salam, how can I help?"

    # 🔹 Vérifier si c'est une question produit
    product_response = handle_product_questions(user_input)
    if product_response:
        return product_response

    # 🔹 Vérifier si c'est une demande de visite
    visit_response = handle_visit_request(user_input)
    if visit_response:
        return visit_response

    # 🔹 Vérifier si c'est une négociation de prix
    price_response = handle_price_negotiation(user_input, user_phone)
    if price_response:
        return price_response

    # 🔹 Si aucune réponse trouvée, on interroge GPT-4
    try:
        gpt_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_reply = gpt_response.choices[0].message.content
        return bot_reply
    except Exception as e:
        return "Sorry, I didn’t get that, can you repeat?"

# Test du chatbot en local
if __name__ == "__main__":
    test_phone = "+97412345678"
    test_name = "Ali"
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        bot_response = handle_user_query(user_message, test_phone, test_name)
        print(f"Chatbot: {bot_response}")
