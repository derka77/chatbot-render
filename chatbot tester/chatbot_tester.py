import random
import unidecode
from test_listing import *  # Importer les données du produit depuis test_listing.py

# Simule les réponses du chatbot sans passer par Twilio

def chatbot_response(user_message):
    user_message = unidecode.unidecode(user_message.strip().lower())
    
    if any(word in user_message for word in ["price", "how much", "cost"]):
        return f"The price is {price} QAR. Let me know if you’re interested!"
    elif any(word in user_message for word in ["model", "which model", "specs", "version"]):
        return f"This is a {title} ({category}), {description}."
    elif any(word in user_message for word in ["visit", "see", "appointment", "check"]):
        slots_text = "\n".join([f"- {slot}" for slot in available_slots])
        return f"The product is available for viewing at {location}. Available slots:\n{slots_text}\nLet me know when you'd like to visit!"
    elif any(word in user_message for word in ["buy", "confirm", "purchase"]):
        return f"Great! Deal confirmed at {price} QAR. The seller will contact you soon: {seller_contact}"
    elif any(word in user_message for word in ["location", "where", "address"]):
        return f"The product is located at {location}. Google Maps link: {location_map_url}"
    elif any(word in user_message for word in ["condition", "used or new", "status"]):
        return f"The product is in {condition} condition."
    elif any(word in user_message for word in ["hello", "hi", "hey"]):
        return random.choice(["Hello! How can I help today?", "Hey there! Need any details?", "Hi! Let me know if you need anything."])
    else:
        return "Sorry, I didn’t understand. Can you rephrase?"

# Boucle de test interactive
def start_chatbot():
    print("Chatbot Tester - Type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    start_chatbot()
