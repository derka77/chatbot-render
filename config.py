# config.py

FORBIDDEN_WORDS = {
    "bro": "Hello",  # Remplace "bro" par "Hello"
    "u": "you",  # Remplace "u" par "you"
    "seller": "I",  # L'acheteur doit penser qu'il parle directement au vendeur
}

PRICE_REMINDER = "I remind you the price is {price} QAR. What offer do you have in mind?"

APPOINTMENT_MESSAGE = (
    "I remind you the price is {price} QAR.\n\n"
    "Here are the available slots:\n{slots}\n\n"
    "Location: {location} ({location_map_url})\n"
    "Contact me at {seller_contact} to confirm."
)

CONFIRMATION_MESSAGE = "I booked {day} with you at {time}. Please confirm."

RESPONSE_VARIANTS = [
    "I didn’t get that, can you say again?",
    "Sorry, I didn’t catch that, can you repeat?",
    "I didn’t understand, say again?"
]

FOLLOW_UP_VARIANTS = [
    "I will come back to you soon",
    "Let me check and I will come back",
    "Give me a moment I will get back to you"
]

