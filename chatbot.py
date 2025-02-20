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

# Détection automatique des catégories
def detect_product_category(user_input):
    CATEGORY_KEYWORDS = {
        "vehicules": ["car", "motorcycle", "bike", "boat", "parts", "accessories", "van", "caravan"],
        "mode": ["clothes", "shoes", "fashion"],
        "luxe": ["jewelry", "watch", "bag", "luxury"],
        "maison": ["furniture", "appliance", "decoration", "garden", "DIY"],
        "multimedia": ["phone", "laptop", "console", "TV", "tablet", "camera"],
        "loisirs": ["book", "music", "sport", "game", "toy", "collectible"],
        "bebe": ["baby", "stroller", "crib", "diaper"],
        "beaute": ["perfume", "cosmetics", "skincare", "wellness"]
    }
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in user_input for keyword in keywords):
            return category
    return "general"

# Gestion des réponses dynamiques par catégorie
def get_dynamic_response(user_input, category):
    RESPONSES = {
        "vehicules": {
            "performance": ["The engine runs smoothly no issues", "No mechanical problems at all"],
            "condition": ["No accidents well maintained", "Clean and well serviced"],
            "age": ["It’s from 2021 still in good shape", "Recent model in great condition"]
        },
        "multimedia": {
            "performance": ["Works perfectly no issues", "Very fast and responsive"],
            "battery": ["Battery lasts long hours", "Battery life is very good"],
            "condition": ["No scratches or broken screen", "Very well maintained like new"]
        },
        "mode": {
            "condition": ["No stains no tears perfect condition", "Looks new and well maintained"],
            "size": ["It’s size M fits well", "Standard size very comfortable"]
        }
    }
    for intent, responses in RESPONSES.get(category, {}).items():
        if intent in user_input:
            return random.choice(responses)
    return None

# Gestion de la conversation principale
def handle_user_query(user_input, user_phone, user_name=""):
    user_input = unidecode.unidecode(user_input.strip().lower())
    save_conversation(user_phone, user_input)

    # Gestion des salutations
    GREETINGS = {
        "hello": ["Hello how can I help", "Hi there how can I assist you"],
        "hi": ["Hi how can I help", "Hey how's it going"],
        "how are you": ["I'm good thanks how can I assist you", "I'm fine how can I help"],
        "you feel well": ["I'm good thanks how can I assist you", "I'm fine how can I help"],
        "morning": ["Good morning how can I assist you", "Morning how can I help"],
        "good evening": ["Good evening how can I assist you", "Good evening how can I help"],
        "good morning": ["Good morning how can I assist you", "Good Morning how can I help"]
    }

    if user_input in GREETINGS:
        return random.choice(GREETINGS[user_input])


    if user_input.startswith("salam"):
        return "wa aleykoum salam how can I help"
    
    category = detect_product_category(user_input)
    dynamic_response = get_dynamic_response(user_input, category)
    if dynamic_response:
        return dynamic_response

    GENERAL_RESPONSES = {
        "battery": ["Battery lasts long hours", "Battery performance is very good"],
        "condition": ["No scratches no damage", "Very well maintained"],
        "accessories": ["Comes with original accessories", "I have everything that was included"],
        "reason": ["Selling because I don’t need it anymore", "Just upgrading to a new one"],
        "test": ["Yes you can check it before buying", "Of course testing is possible"],
        "price": [f"I was looking for {price} QAR but I might adjust", f"The price is {price} QAR but I can consider offers"]
    }
    
    match = process.extractOne(user_input, GENERAL_RESPONSES.keys(), scorer=fuzz.partial_ratio)

    if match and len(match) >= 2:  # Vérifie que le match contient bien 2 éléments
        best_match, score = match[:2]  # Sécurisation du déballage des valeurs
        if score > 50:  # Abaisser le seuil pour éviter trop de rejets
            return random.choice(GENERAL_RESPONSES[best_match])

    # Si aucune intention claire n'est trouvée, proposer une réponse générique
    return "I'm not sure I understood, but the product is available. Let me know if you need details."


    if score > 75:
        return random.choice(GENERAL_RESPONSES[best_match])
    
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
