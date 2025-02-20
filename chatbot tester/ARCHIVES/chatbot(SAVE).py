import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model, brand, material, dimensions

# ⚡️ Gestion des échanges et confirmations
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}

# Twilio Client pour envoyer les messages
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# 🔄 Liste des mots-clés fixes
greetings_keywords = ["hi", "hello", "hey", "salam", "bonjour", "good morning", "good evening", 
                      "how are you", "what's up", "yo", "greetings", "hola", "salutations", 
                      "hey there", "hi there", "good afternoon", "evening", "morning", "sup"]

model_keywords = ["model", "which model", "what model", "which version", "product model", "which type", 
    "specs", "configuration", "technical details", "which specs", "what type", "what version",
    "which model is this", "can you tell me the model", "is this the latest model", 
    "is this an old model", "which version", "is it an updated model", 
    "does it have the latest features", "any special specs", "what are the features"]

year_keywords = ["year", "which year", "model year", "what year", "production year", "release year", 
    "how old is it?", "what year was it made", "when was it produced", "when was it released", 
    "manufacturing year", "is it from this year", "was it released this year", "is it the latest model"]

condition_keywords = [
    "used or new", "is it new or used", "is it in good condition", "is it still in good shape",
    "how used is it", "has it been used often", "how often was it used", "was it heavily used",
    "does it work fine", "does it function properly", "is it in perfect working condition",
    "is it slightly used", "does it have any scratches", "any signs of wear",
    "has it been used a lot", "is it in mint condition", "is it like new", "how many times was it used"]

usage_keywords = [
    "used often", "how often used", "how many times used", "is it heavily used", 
    "does it still work", "does it function properly", "is it in working condition", 
    "any signs of wear", "is it still reliable", "does it perform well", 
    "any wear and tear", "has it been used a lot", "how long has it been used", 
    "is it lightly used", "is it in mint condition", "is it well maintained", 
    "does it have any issues", "is it in perfect working order"]

price_keywords = [
    "what is the price", "how much", "price", "can I get a discount", "is the price negotiable",  
    "last price", "final price", "discount available", "best price", "any discount",  
    "lowest price", "how much is this", "how much are you asking", "is this firm price",  
    "can you lower the price", "cheaper price", "can we negotiate", "is it on sale",  
    "can you do better on price", "what's your best offer", "what's your lowest offer",  
    "any promo", "any special offer", "can I get a deal", "bulk price", "combo price",  
    "can I make an offer", "would you accept", "is there any room for negotiation"]

payment_keywords = [
    "do you accept cash", "how can I pay", "payment methods", "can I pay online", "card payment",  
    "do you take PayPal", "can I pay in installments", "cash only?", "do you take credit card?",  
    "can I pay by bank transfer?", "is PayPal okay?", "do you accept Apple Pay?", "can I pay with Google Pay?",  
    "do you take cryptocurrency?", "do you accept checks?", "is cash preferred?",  
    "can I pay later?", "deposit required?", "is there a down payment?",  
    "can I pay half now and half later?", "do you offer payment plans?", "is there a fee for card payments?",  
    "what's the easiest way to pay?", "do you take mobile payments?", "do you accept contactless payment?",  
    "do you have a QR code for payment?", "can I pay upon delivery?", "is it pay before or after?",  
    "do I need to send proof of payment?"]

guarantee_keywords = [
    "is there a warranty", "how long is the warranty", "any warranty included", "guarantee period",  
    "does it come with a warranty?", "is there any guarantee?", "how long does the guarantee last?",  
    "warranty available?", "what does the warranty cover?", "is it under warranty?",  
    "can I get an extended warranty?", "do you offer a money-back guarantee?", "is there a refund policy?",  
    "can I return it if it doesn’t work?", "what if it breaks?", "any repair guarantee?",  
    "is there a manufacturer warranty?", "do I get a receipt for warranty?",  
    "is the warranty transferable?", "how do I claim the warranty?", "who handles warranty repairs?",  
    "is there a replacement policy?", "what is your return policy?", "is there a service warranty?",  
    "does the guarantee include free repairs?", "can I exchange it if faulty?", "is there a trial period?",  
    "what happens if it stops working?", "does it cover accidental damage?"]

authenticity_keywords = [
     "is it original", "is this fake", "is it authentic", "genuine product", "official brand",  
    "is it a copy", "does it have a certificate", "is this real?", "is it certified?",  
    "how can I verify it's real?", "is this the official version?", "is it factory sealed?",  
    "does it come with proof of authenticity?", "can you provide a certificate?",  
    "is it a replica?", "is it first-hand or second-hand?", "is it brand new or refurbished?",  
    "does it have the official logo?", "is it made by the original manufacturer?",  
    "does it come with an authenticity card?", "is this a limited edition?",  
    "can you show the serial number?", "is this licensed?", "does it come in original packaging?",  
    "does it have a hologram sticker?", "is it approved by the brand?",  
    "is there a way to check its authenticity?", "is it handmade or mass-produced?",  
    "does it match official specifications?", "is it collector's edition?",  
    "has it been verified by an expert?", "is this a genuine resale?"]

car_electronics_keywords = [
    "mileage", "fuel type", "engine capacity", "battery life", "screen size",  
    "RAM and storage", "processor type", "horsepower", "transmission type", "manual or automatic",  
    "year of manufacture", "service history", "any accidents?", "number of previous owners",  
    "car condition", "is it refurbished?", "warranty available?", "charging time",  
    "USB ports", "Bluetooth support", "WiFi capability", "touchscreen display",  
    "navigation system", "does it support Apple CarPlay?", "does it have Android Auto?",  
    "parking sensors", "rearview camera", "cruise control", "sound system brand",  
    "speaker quality", "headlight type", "fuel efficiency", "electric or hybrid?",  
    "battery replacement cost", "does it come with original accessories?",  
    "any scratches or dents?", "is the software upgradable?", "does it have a fingerprint sensor?",  
    "water resistance rating", "4K or Full HD display?", "does it support fast charging?",  
    "how long does the battery last?", "how many charging cycles?",  
    "touchscreen sensitivity", "is it factory unlocked?", "is it compatible with my network?",  
    "what’s the refresh rate?", "is it gaming-compatible?", "expandable storage?",  
    "does it have a CD/DVD player?", "does it come with a charger?",  
    "does it have noise cancellation?", "is the screen OLED or LCD?"]

visit_test_keywords = [
    "can I test it", "can I see it working", "is a demo possible", "try before buy",  
    "can I visit to check", "can I inspect it?", "can I come and see?", "is a trial available?",  
    "can I check it in person?", "can I try it first?", "is it possible to test before buying?",  
    "can I come and test it?", "can I see how it works?", "can you show me a video of it working?",  
    "do you offer test drives?", "can I come and take a look?", "is a hands-on test possible?",  
    "can I see it in action?", "can I visit your location?", "do you allow in-person testing?",  
    "can I come to your store?", "is there a showroom?", "can I come and inspect?",  
    "do you have a demo unit?", "can you demonstrate how it works?", "is an on-site test possible?",  
    "can I check the condition before paying?", "can I verify it works properly?",  
    "can I test all the features?", "can I see it before making a decision?"]

availability_keywords = ["still available", "is this available", "do you still have it", "is it in stock",  
    "can I buy it now", "is it already sold", "is it reserved", "is it gone",  
    "is this item taken?", "is this still up for sale?", "can I still get this?",  
    "do you have more in stock?", "is this the last one?", "any left?",  
    "is it pending pickup?", "is this listing active?", "has it been claimed?",  
    "is someone else buying it?", "is this currently available?",  
    "can I come pick it up now?", "do you have another one?", "any available units?",  
    "can you hold it for me?", "can I pre-order?", "is there a waiting list?",  
    "is it backordered?", "is this discontinued?", "how many do you have left?",  
    "is this limited stock?", "when will it be back in stock?", "is this brand new or leftover stock?"]

shipping_keywords = ["do you deliver", "can you ship", "shipping cost", "delivery fee", "how much for shipping",  
    "is shipping included?", "do you offer free shipping?", "how long does shipping take?",  
    "do you deliver to my area?", "can I pick it up?", "is local pickup available?",  
    "what are the delivery options?", "do you use express shipping?", "can you send it by mail?",  
    "which courier do you use?", "do you ship internationally?", "how soon can you ship?",  
    "can I choose the shipping method?", "do you provide tracking?", "is there a tracking number?",  
    "who pays for shipping?", "can I pay on delivery?", "do you offer same-day delivery?",  
    "is next-day delivery available?", "can I schedule delivery?", "do you use insured shipping?",  
    "can I send my own courier?", "do you deliver on weekends?", "can I get an estimated delivery date?",  
    "how do I track my order?", "do you provide packaging?", "is the shipping safe?",  
    "do you offer cash on delivery?", "can you send it through FedEx/UPS/DHL?",  
    "what’s the cheapest shipping option?", "do you offer bulk shipping rates?"]

accessories_keywords = ["does it come with", "what’s included", "any extra parts", "does it have accessories",  
    "is the charger included", "does it come with a case", "does it include the box",  
    "are all original accessories included?", "does it have all parts?", "any missing parts?",  
    "does it come with a manual?", "are extra cables included?", "does it include earphones?",  
    "is the power adapter included?", "does it have a remote control?",  
    "is there a warranty card?", "does it come with a stand?", "does it have extra batteries?",  
    "does it include a strap?", "does it come with extra filters?", "are extra lenses included?",  
    "does it come with a carrying bag?", "is there a protective cover?",  
    "does it include software or license key?", "does it have a mounting kit?",  
    "is the SIM card included?", "does it come with extra brushes?", "are there any free add-ons?",  
    "do I get a screen protector with it?", "does it include a keyboard and mouse?",  
    "does it come with a dock or stand?", "are cables and adapters included?",  
    "does it come fully assembled?", "is a memory card included?", "does it have a belt clip?",  
    "are there additional attachments?", "does it come with a cleaning cloth?"]

location_keywords = ["where are you located", "where can I pick it up", "what’s the address",  
    "where to meet", "is pickup possible", "can we meet somewhere?",  
    "where do I go?", "can I collect it in person?", "pickup location?",  
    "is local pickup available?", "can you share your location?",  
    "do you have a store?", "where is your shop?", "where do you deliver from?",  
    "is there a meeting point?", "can we meet halfway?", "do you have a fixed pickup spot?",  
    "what’s the nearest landmark?", "can I pick it up at your house?",  
    "do you offer curbside pickup?", "is pickup free?", "do you have a warehouse?",  
    "can we meet at a public place?", "where should I come?", "is there a safe pickup spot?",  
    "can I choose the meetup location?", "can I pick up today?", "where exactly are you?",  
    "how far are you from my location?", "is it safe to meet there?", "is parking available?",  
    "can I pick it up from your office?", "do you offer contactless pickup?",  
    "is pickup available on weekends?"]

# 📌 Ajout de RESPONSE_VARIATIONS AVANT son utilisation
RESPONSE_VARIATIONS = {
    "greetings": ["Hello! How can I help you?", "Hey! Need any help?", "Salam! How can I assist you?",  
    "Hi there! What can I do for you?", "Hello, what information do you need?",  
    "Hey! Let me know how I can assist you.", "Hi! How’s it going? Need any details?",  
    "Hello! Feel free to ask any questions.", "Hey there! How can I be of service?",  
    "Hi! What do you need help with?", "Hey, what can I do for you today?", "Hello! Do you have any questions?",  
    "Hi there! Let me know if you need any info.", "Hello! Looking for something? Let me know!", "Hi! What are you interested in?",  
    "Hey! I’d be happy to help. What do you need?", "Hi! How can I make this easier for you?",  
    "Hello! Ready to assist. What’s on your mind?"],

    response_templates = {
    "model": [
        "This is the {brand} {title}", "You're looking at a {title} from {brand}",
        "The model is {title}, manufactured by {brand}", "This {brand} {title} is a great choice",
        "You are viewing a {title} by {brand}", "This {title} is a genuine product from {brand}",
        "The {title} is a well-known model from {brand}", "This {brand} {title} is highly rated"
    ],

    "year": [
        "This model was released in {year_model}", "The production year is {year_model}",
        "This {title} was manufactured in {year_model}", "It was made in {year_model}",
        "The {title} is from {year_model}", "This unit dates back to {year_model}",
        "It has been in production since {year_model}", "Originally built in {year_model}"
    ],

    "condition": [
        "It's in {condition} condition", "The item is {condition}", "It's a {condition} product",
        "This is a {condition} item", "The overall condition is {condition}",
        "Expect a {condition} condition.", "It has been well maintained and is {condition}",
        "This product is still in {condition} shape"
    ],

    "availability": [
        "Yes, the item is still available!", "It's still for sale", "Yes, you can still buy this item",
        "Yes, it's available", "This item hasn’t been sold yet", "Still up for grabs!",
        "Yes, it's on sale and available", "It's currently available, let me know if you're interested"
    ],

    "shipping": [
        "Sorry, shipping is not available\nPick-up is required",
    "I can't offer delivery at the moment\nThis item is for local pickup only",
    "Shipping is not an option for this item\nYou will need to pick it up",
    "Unfortunately, I do not offer shipping\nThe item must be collected in person",
    "No shipping available\nThe item can only be picked up from {location}",
    "This item is only available for pickup\nNo delivery service is offered",
    "I do not ship this item\nPlease arrange for a pickup",
    "Pick-up only\nShipping is not available for this item"
    ],

    "accessories": [
        "It comes with all original accessories.", "The package includes {accessories}",
        "Yes, it includes {accessories}.", "Everything that came in the box is included",
        "Accessories included: {accessories}.", "Comes with {accessories} as part of the package",
        "Yes, {accessories} are part of the deal.", "You’ll receive {accessories} with this purchase"
    ],

    "location": [
        "The item is available at {location}.", "You can pick it up from {location}",
        "Meet-up is possible at {location}.", "Location: {location}",
        "You can collect it at {location}.", "Pick-up point: {location}",
        "We can arrange a meet-up at {location}.", "This item is located in {location}"
    ],
    
    "price": [
        "The price is {price}. Let me know if you’re interested!", "It’s currently available for {price}",
        "I'm selling this for {price}.", "The asking price is {price}",
        "Price is set at {price}.", "You can get this for {price}",
        "This item costs {price}.", "The listed price is {price}"
    ],

    "payment": [
        "Payment is usually discussed on-site. Cash and local transactions are preferred",
        "We accept cash and local payments.", "Cash on pickup is preferred",
        "Payment options can be discussed.", "Payments can be made in person",
        "Cash and standard payment methods accepted.", "You can pay upon collection",
        "We can talk about payment arrangements when you decide to buy"
    ],

    "guarantee": [
        "This product comes with a {warranty_period} warranty", 
        "A warranty of {warranty_period} is included",
        "You get a {warranty_period} warranty with this item", 
        "This item is covered under a {warranty_period} warranty",
        "Warranty coverage lasts for {warranty_period}", 
        "The product includes a {warranty_period} manufacturer warranty",
        "You'll have a {warranty_period} guarantee on this", 
        "Warranty period: {warranty_period}"
    ],

    "authenticity": [
        "This is an original {brand} product. It comes with {authenticity_certificate}",
        "Authenticity guaranteed: {brand} {title}.", "This is a genuine {brand} item",
        "Yes, it's 100% authentic from {brand}.", "It has been verified as an original {brand} product",
        "Comes with proof of authenticity: {authenticity_certificate}", 
        "This is not a replica—it's an authentic {brand} item",
        "You will receive an authenticity certificate: {authenticity_certificate}"
    ],

    "car_electronics": [
        "It has {mileage} km and runs on {fuel_type}.", "The battery life is around {battery_life}",
        "This vehicle has {mileage} km on it.", "Fuel type: {fuel_type}",
        "Battery condition: {battery_life}.", "It features a powerful {engine_capacity} engine",
        "The mileage is {mileage}, and it's in good condition", 
        "Runs efficiently with {fuel_type} and {battery_life} battery life"
    ],

    "visit_test": [
        "You can visit to check and test it. Let’s schedule a time!", 
        "A demo is possible, let me know when you want to visit",
        "Feel free to come and test it.", "You are welcome to try before buying",
        "Testing is allowed before purchase.", "We can arrange a time for you to see it working",
        "I can show you how it works before you decide.", "Demo available upon request"
    ]
}

# 📌 Fonction principale de gestion des requêtes
def handle_user_query(user_input, user_phone):
    user_input = unidecode.unidecode(user_input.strip().lower())
    user_conversations.setdefault(user_phone, []).append(user_input)

    # Détection des salutations
    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in greetings_keywords):
        return random.choice(RESPONSE_VARIATIONS["greetings"])

    # Détection des autres mots-clés et formatage des réponses avec .format()
    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in model_keywords):
        return random.choice(RESPONSE_VARIATIONS["model"]).format(title=title, brand=brand)

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in year_keywords):
        return random.choice(RESPONSE_VARIATIONS["year"]).format(year_model=year_model, title=title)

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in condition_keywords):
        return random.choice(RESPONSE_VARIATIONS["condition"]).format(condition=condition)
    
    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in price_keywords):
        return random.choice(RESPONSE_VARIATIONS["price"]).format(price=price)

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in payment_keywords):
        return random.choice(RESPONSE_VARIATIONS["payment"])

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in guarantee_keywords):
        return random.choice(RESPONSE_VARIATIONS["guarantee"])

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in authenticity_keywords):
        return random.choice(RESPONSE_VARIATIONS["authenticity"]).format(brand=brand, authenticity_certificate="Yes")

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in car_electronics_keywords):
        return random.choice(RESPONSE_VARIATIONS["car_electronics"]).format(mileage="50,000", fuel_type="Petrol", battery_life="8 hours")

    if any(re.search(r'\b' + re.escape(keyword) + r'\b', user_input) for keyword in visit_test_keywords):
        return random.choice(RESPONSE_VARIATIONS["visit_test"])

    return random.choice(["Not sure, can you clarify?", "Say again?", "I didn’t get that, try another way",  
    "Could you rephrase that?", "Sorry, I didn’t catch that",  
    "Can you say it differently?", "I need more details",  
    "I don’t understand, can you explain?", "That wasn’t clear, try again",  
    "Can you be more specific?"])

# Proposer un RDV
def propose_appointment_slots(user_phone):
    slots_text = "\n".join([f"- {slot}" for slot in available_slots])
    message_variants = [
        f"Here are the available time slots\n{slots_text}\n\nTo proceed, please contact me directly at {seller_contact}\nLocation: {location}",
        f"I’m available at these times\n{slots_text}\n\nPlease reach out to me at {seller_contact} to confirm\nLocation: {location}",
        f"When would you like to meet? Here are my available slots\n{slots_text}\n\nI won't be able to reply here, so please call or message me at {seller_contact} to finalize\nLocation: {location}",
        f"Available meeting times\n{slots_text}\n\nFor confirmation, kindly message me directly at {seller_contact} I won't be able to confirm here\nLocation: {location}",
        f"To set up a meeting, here are my available slots\n{slots_text}\n\nPlease contact me at {seller_contact}, as I can't finalize appointments in this chat\nLocation: {location}"
    ]
    
    return random.choice(message_variants)

# 💡 Transfert à un humain après 3 échecs cumulés
def transfer_to_human(user_phone):
    # Compter le nombre total d'échecs en vérifiant chaque phrase d’incompréhension
    failure_count = sum(user_conversations[user_phone].count(phrase) for phrase in unclear_responses)

    if failure_count >= 3:
        try:
            twilio_client.messages.create(
                from_="whatsapp:+14155238886",
                to=f"whatsapp:{seller_contact}",
                body=f"A buyer is asking questions but I couldn’t assist. Here’s the chat history: {user_conversations[user_phone]}"
            )
            
            # Variantes de réponse pour masquer le transfert en douceur
            response_variants = [
                "Sorry, I’m a bit tied up at the moment. I’ll get back to you shortly",
                "Let me check that for you. I’ll come back to you in a moment",
                "I might have missed something. Give me a second, I’ll get back to you",
                "I’ll need a moment to check that. I’ll be right back",
                "Let me take a quick look and I’ll get back to you",
                "I’m just finishing something up, I’ll reply soon",
                "Let me sort this out and I’ll update you shortly",
                "I might need to confirm something, I’ll return to you soon"
            ]
            
            return random.choice(response_variants)
