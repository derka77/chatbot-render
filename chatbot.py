import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model, location_map_url
from rapidfuzz import process, fuzz

# Historique des échanges
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}

twilio_client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

def humanize_text(text, add_typo=False):
    text = text.replace("i am", "im").replace("what is", "whts").replace("this is", "dis is").replace("it's", "its")
    if add_typo and random.random() < 0.2:
        text = text.replace("the", "da").replace("and", "n").replace("to", "2")
    return text

def convert_price_format(price_str):
    price_str = price_str.lower().replace("qar", "").replace(",", "").strip()
    match = re.search(r'(\d+)\.?([0-9]*)k', price_str)
    if match:
        thousands = int(match.group(1)) * 1000
        hundreds = int(match.group(2)) * 100 if match.group(2) else 0
        return thousands + hundreds
    match = re.search(r'\b\d+\b', price_str)
    if match:
        return int(match.group(0))
    return None

def handle_price_negotiation(user_input, user_phone):
    offer = convert_price_format(user_input)
    if offer is not None:
        if offer < min_price:
            return "sory  too low cant do"
        user_conversations[user_phone].append(f"offer detectd: {offer} QAR")
        return f"so you say {offer} QAR? let me know and I will check if possible"

    return random.choice(["not sure abt that you mean price?", "could you clarify, you mean the price?", "i didn't get that, are you asking about the price?"])

def propose_appointment_slots():
    slots_text = "\n".join([f"{slot.replace('.', '')}" for slot in available_slots])
    return f"you can visit price is {price} QAR\navailable times:\n" + slots_text + "\nconfirm fast contact {seller_contact}"

def handle_visit_request(user_input, user_phone):
    visit_keywords = ["can i visit", "can i check", "see it", "meet to view"]
    if any(request in user_input for request in visit_keywords):
        response = propose_appointment_slots()
        if user_conversations[user_phone][-1].startswith("you can visit"):
        response = f"Just a reminder, price is {price} QAR"
        return response
    return None

def send_seller_summary(user_phone, user_name, offer_price=None, selected_slot=None):
    conversation_summary = " ".join(user_conversations[user_phone][-3:])
    summary = (
        f"new buyer\n"
        f"name: {user_name}\n"
        f"phone: {user_phone}\n"
        
        f"offer: {offer_price if offer_price else 'no offer yet'}\n"
        
        f"time: {selected_slot if selected_slot else 'not confirmd'}\n"
        f"context: Showed interest, asked for details, confirmed visit, discussed price"
        f"contact at this number for confirm {seller_contact}"
    )
    print(f"sent to seller: {summary}")
    return random.choice([f"ok {user_name}, your details sent, expect a call soon", f"got it {user_name}, details forwarded, you should receive a call soon", f"info sent {user_name}, you will be contacted soon"])

def handle_user_query(user_input, user_phone, user_name=""):
    details_keywords = ["more details", "tell me more", "need info"]
    if any(keyword in user_input for keyword in details_keywords):
        return f"{description}"
    user_input = unidecode.unidecode(user_input.strip().lower())
    user_conversations.setdefault(user_phone, []).append(user_input)
    
    for handler in [lambda inp: handle_visit_request(inp, user_phone), lambda inp: handle_price_negotiation(inp, user_phone)]:
        response = handler(user_input)
        if response:
            return response
    
    return random.choice(["hmm not sure, say again", "could you rephrase?", "not sure what you mean, try again"])

if __name__ == "__main__":
    test_phone = "+97412345678"
    test_name = "Ali"
    while True:
        user_message = input("you: ")
        if user_message.lower() in ["exit", "quit"]:
            break
        bot_response = handle_user_query(user_message, test_phone, test_name)
        print(f"chatbot: {bot_response}")
