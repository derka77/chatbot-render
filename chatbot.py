import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import (
    title, category, description, price, location, min_price,
    seller_contact, image_url, available_slots, condition, year_model, location_map_url
)
from config import FORBIDDEN_WORDS, RESPONSE_VARIANTS, FOLLOW_UP_VARIANTS
from rapidfuzz import process, fuzz

# Historique des échanges
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}
buyer_attempts = {}

# Configuration de Twilio
twilio_client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

# Nettoyage du texte
def clean_text(text):
    for word, replacement in FORBIDDEN_WORDS.items():
        text = text.replace(word, replacement)
    return text

# Enregistrer conversations pour statistiques
def save_conversation(user_phone, message):
    user_conversations.setdefault(user_phone, []).append(message)

# Convertir une offre de prix en entier
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
    return None

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

# Détection des questions sur l'annonce avec RapidFuzz
def detect_question(user_input):
    question_patterns = {
        "performance": ["does this laptop work well", "any problem", "is it working fine"],
        "battery": ["how long battery last", "battery drain fast", "good battery"],
        "reason_sale": ["why you sell", "why selling"],
        "accessories": ["you have box and charger", "any accessories"],
        "condition": ["any scratches", "screen broken", "good condition"],
        "age": ["how old is laptop", "year bought"],
        "test_before_buy": ["can i test before buy", "try it first"],
        "price_negotiation": ["can you lower price", "final price"],
        "more_pictures": ["send more pictures", "can i see more photos"],
        "original_model": ["is original model or copy", "genuine or fake"],
        "delivery": ["can you deliver", "home delivery available"]
    }

    best_match = None
    best_score = 0
    for category, questions in question_patterns.items():
        match, score, _ = process.extractOne(user_input, questions, scorer=fuzz.partial_ratio)
        if score > best_score:
            best_match = category
            best_score = score

    return best_match if best_score > 75 else None

# Réponses associées aux questions détectées
def get_answer_for_question(question_category):
    answers = {
        "performance": "Yes, it works perfectly, no issues at all.",
        "battery": "The battery life is great, lasts several hours without any issue.",
        "reason_sale": "I just don’t use it much, so I decided to sell.",
        "accessories": "Yes, it comes with the original box and charger.",
        "condition": "No scratches, no damage. The screen is in perfect condition.",
        "age": f"It was bought in {year_model}, so it’s still quite new.",
        "test_before_buy": "Yes, of course. If you're interested, you can check it during the visit.",
        "price_negotiation": f"I was looking for {price} QAR, but I might adjust a little. What’s your best offer?",
        "more_pictures": f"Sure! Here’s a picture: {image_url}",
        "original_model": "It’s the original Apple MacBook Pro.",
        "delivery": "I prefer to meet in person so you can check the laptop first."
    }
    return answers.get(question_category, None)

# Gestion de la conversation principale
def handle_user_query(user_input, user_phone, user_name=""):
    user_input = unidecode.unidecode(user_input.strip().lower())
    save_conversation(user_phone, user_input)

    # Salam en premier
    if user_input.startswith("salam"):
        return "wa aleykoum salam, how can I help?"

    # Détecter la question avec RapidFuzz
    question_category = detect_question(user_input)
    if question_category:
        return clean_text(get_answer_for_question(question_category))

    # Vérifier les demandes de visite
    visit_response = handle_visit_request(user_input, user_phone)
    if visit_response:
        return visit_response

    # Vérifier les négociations de prix
    price_response = handle_price_negotiation(user_input, user_phone)
    if price_response:
        return price_response

    # Sinon, réponse générique intelligente
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
