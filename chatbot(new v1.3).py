import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model, location_map_url

from rapidfuzz import process, fuzz

# 🔴 Historique des échanges et confirmations
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}
pending_confirmations = {}  # Stocke les utilisateurs en attente de confirmation d'un prix
pending_visits = {}  # Stocke les utilisateurs qui ont demandé une visite mais pas encore confirmé

location_map_url = "https://maps.app.goo.gl/TzFqJmMTwx6iRoMG9"

# ✅ Connexion à Twilio
twilio_client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

def clean_user_input(user_input):
    """Nettoie le texte utilisateur : supprime la ponctuation, accents et met en minuscule"""
    user_input = unidecode.unidecode(user_input.strip().lower())  # Supprime accents, majuscules
    user_input = re.sub(r'[^\w\s]', '', user_input)  # Supprime toute la ponctuation
    return user_input


# ✅ GESTION DES SALUTATIONS
def handle_greetings(user_input):
    greetings = ["gud evening", "heyy", "salut", "hello", "salut", "good morning", "salm", "good evening", "gud morning", "hi", 
    "bonjor", "salm", "gud evening", "heyy", "hi", "gud evening", "hey", "bonjor", "good morning", "hii", 
    "hii", "salem", "slt", "salam", "slt",  "bonjour", "hey", "bonjour", "slt", "gud morning", "slam"]

    if any(word in user_input for word in greetings):
        return random.choice([
            "Hello! How can I help you?", "Hi there! What can I do for you?", "Salam! How can I assist you?",
            "Hey! Need any help?", "Greetings! How may I assist?", "Hi", "Hello", "Salam, Need any information"
        ])
    return None

# ✅ GESTION DES INFORMATIONS PRODUIT
def handle_product_info(user_input):
    """Gère les questions sur l'année, le modèle et l'état du produit"""
    
    model_keywords = [
        "model", "which model", "what model", "which version", "product model", "which type",
        "specs", "configuration", "technical details", "which specs", "what type", "what version",
        "which model is this", "which model it is", "can you tell me the model", "is this the latest model",
        "is this an old model", "which version is it", "is it an updated model",
        "does it have the latest features", "any special specs", "what are the features"
    ]
    
    year_keywords = [
        "year", "which year", "model year", "what year", "production year", "release year",
        "how old is it?", "what year was it made", "when was it produced", "when was it released",
        "manufacturing year", "is it from this year", "was it released this year", "is it the latest model"
    ]
    
    # ✅ Vérification stricte AVANT fuzzy matching
    clean_input = user_input.lower().strip()
    
    if clean_input in model_keywords:
        return f"The model is {title}. It features {description}."
    
    if clean_input in year_keywords:
        return f"This product was manufactured in {year_model}. It’s in {condition} condition."

    # ✅ Correction ici : récupérer trois valeurs au lieu de deux
    best_match = process.extractOne(clean_input, model_keywords + year_keywords, scorer=fuzz.partial_ratio, score_cutoff=70)

    if best_match:
        match, score, _ = best_match  # ✅ Ignorer la troisième valeur qui pose problème

        if match in model_keywords:
            return f"The model is {title}. It features {description}."
        
        if match in year_keywords:
            return f"This product was manufactured in {year_model}. It’s in {condition} condition."

    return None  # ❌ Si aucun mot clé ne correspond, laisser le reste du chatbot gérer

    condition_keywords = ["how much status of this?", "when is it used happen", 
    "how much is it in good condition", "is it used detail", "whitch is it new", 
    "is it in good condition", "is it new detail", "is it new", "iz it in good condition", 
    "condition", "prduct condition?", "why condition matter", 
    "what condition? detail", "when condition happen", "when is it used happen", 
    "condition detail", "tell me status of this?", "what abt used or new", "what condition? detail", "why used or new matter", 
    "iz it in good condition", "iz it used", 
    "how much used or new", "status of this?", 
    "iz it in good condition", "iz it new", "iz it used", 
    "iz it new", "sttus of this?", "tell me is it new", "tell me product condition?", "why is it used matter", 
    "how much is it new", "tell me is it in good condition", "wat condition?", 
    "iz it used", "tell me condition", 
    "what abt is it used", "what abt product condition?", 
    "is it used", "when product condition? happen", 
    "wht is it used", "wht what condition?", 
    "condition", "wht is it in good condition", "yer product condition?", 
    "how much used or new", "why is it in good condition matter", 
    "is it new detail", "tell me status of this?", 
    "how much used or new", "what abt is it new", 
    "how much is it new", "is it in good condition detail", "prduct condition?", "used or new detail", "when condition happen", 
    "tell me status of this?", "why used or new matter", 
    "is it used detail", "whitch product condition?", "whitch status of this?", "wht what condition?", 
    "status of this? detail", "when condition happen", "wht is it used", "why product condition? matter", "yer is it in good condition", 
    "how much is it used", "product condition?", "used or new", "what abt is it new", "why condition matter", 
    "how much used or new", "whitch what condition?", "why used or new matter", "yer is it new", 
    "product condition?", "status of this? detail", "yer product condition?", 
    "whitch is it new", "why is it in good condition matter", "yer is it new", 
    "status of this? detail", "tell me is it in good condition", "used or new detail", "what condition? detail", 
    "when used or new happen", "yer is it in good condition", 
    "wat condition?", "what abt status of this?", "whitch is it in good condition", "whitch product condition?", 
    "condition", "what conditon?", "wht what condition?", "yer is it used", 
    "product conditon?", "whitch is it in good condition", "whitch status of this?", 
    "is it in good condition", "used or new detail", "when is it in good condition happen", "why is it new matter", "yer product condition?", 
    "status of this?", "why product condition? matter", 
    "wht product condition?", "why is it in good condition matter", 
    "when is it in good condition happen", "why is it new matter", 
    "how much condition", "tell me condition", "tell me what condition?", "whitch what condition?", 
    "is it new", "what abt is it new", "why is it in good condition matter", 
    "tell me status of this?", "when product condition? happen", "whitch product condition?", "whitch what condition?", 
    "conditon", "when status of this? happen", 
    "wat condition?", "wht is it in good condition", "yer used or new", 
    "how much product condition?", "iz it new", "wht used or new", 
    "how much is it in good condition", "prduct condition?", "whitch condition", "wht product condition?", 
    "what abt status of this?", "yer is it in good condition", 
    "is it nu", "what abt is it used", "yer used or new", 
    "how much product condition?", "is it in good condition detail", "wht is it new", "wht product condition?", "why what condition? matter", 
    "status of this?", "tell me is it new", "tell me what condition?", "when used or new happen", "yer status of this?", 
    "prduct condition?", "product condition? detail", "tell me condition", "used or new detail", "whitch product condition?", 
    "used or new detail", "what abt is it new", "whitch condition", 
    "tell me used or new", "yer is it new"]

    price_keywords = ["what is the price", "how much", "price", "can I get a discount", "is the price negotiable",  
    "last price", "final price", "discount available", "best price", "any discount",  
    "lowest price", "how much is this", "how much are you asking", "is this firm price",  
    "can you lower the price", "cheaper price", "can we negotiate", "is it on sale",  
    "can you do better on price", "what's your best offer", "what's your lowest offer",  
    "any promo", "any special offer", "can I get a deal", "bulk price", "combo price",  
    "can I make an offer", "would you accept", "is there any room for negotiation"]

    payment_keywords = ["do you accept cash", "how can I pay", "payment methods", "can I pay online", "card payment",  
    "do you take PayPal", "can I pay in installments", "cash only?", "do you take credit card?",  
    "can I pay by bank transfer?", "is PayPal okay?", "do you accept Apple Pay?", "can I pay with Google Pay?",  
    "do you take cryptocurrency?", "do you accept checks?", "is cash preferred?",  
    "can I pay later?", "deposit required?", "is there a down payment?",  
    "can I pay half now and half later?", "do you offer payment plans?", "is there a fee for card payments?",  
    "what's the easiest way to pay?", "do you take mobile payments?", "do you accept contactless payment?",  
    "do you have a QR code for payment?", "can I pay upon delivery?", "is it pay before or after?",  
    "do I need to send proof of payment?"]

    guarantee_keywords = ["is there a warranty", "how long is the warranty", "any warranty included", "guarantee period",  
    "does it come with a warranty?", "is there any guarantee?", "how long does the guarantee last?",  
    "warranty available?", "what does the warranty cover?", "is it under warranty?",  
    "can I get an extended warranty?", "do you offer a money-back guarantee?", "is there a refund policy?",  
    "can I return it if it doesn’t work?", "what if it breaks?", "any repair guarantee?",  
    "is there a manufacturer warranty?", "do I get a receipt for warranty?",  
    "is the warranty transferable?", "how do I claim the warranty?", "who handles warranty repairs?",  
    "is there a replacement policy?", "what is your return policy?", "is there a service warranty?",  
    "does the guarantee include free repairs?", "can I exchange it if faulty?", "is there a trial period?",  
    "what happens if it stops working?", "does it cover accidental damage?"]

    authenticity_keywords = ["is it original", "is this fake", "is it authentic", "genuine product", "official brand",  
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

    car_electronics_keywords = ["mileage", "fuel type", "engine capacity", "battery life", "screen size",  
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

    visit_test_keywords = ["can I test it", "can I see it working", "is a demo possible", "try before buy",  
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

    if any(word in user_input for word in model_keywords):
        return random.choice ([
        f"The model is {title}. It comes with {description}"
        f"model"
        f"This is the {brand} {title}",
        f"You're looking at a {title} from {brand}",
        f"The model is {title}, manufactured by {brand}",
        f"This {brand} {title} is a great choice",
        f"You are viewing a {title} by {brand}",
        f"This {title} is a genuine product from {brand}",
        f"The {title} is a well-known model from {brand}",
        f"This {brand} {title} is highly rated"
        ])

    if any(word in user_input for word in year_keywords):
        return random.choice ([
        f"This product is from {year_model}. It's in {condition} condition",
        f"year",
        f"This model was released in {year_model}",
        f"The production year is {year_model}",
        f"This {title} was manufactured in {year_model}",
        f"It was made in {year_model}",
        f"The {title} is from {year_model}",
        f"This unit dates back to {year_model}",
        f"It has been in production since {year_model}",
        f"Originally built in {year_model}"
        ])

    if any(word in user_input for word in condition_keywords):
        return random.choice ([
        f"This product is in {condition} condition"
        f"It's in {condition} condition",
        f"The item is {condition}",
        f"It's a {condition} product",
        f"This is a {condition} item",
        f"The overall condition is {condition}",
        f"Expect a {condition} condition",
        f"It has been well maintained and is {condition}",
        f"This product is still in {condition} shape"
        ])   

    if any(word in user_input for word in availability_keywords):
        return random.choice ([
        f"Yes, the item is still available!",
        f"It's still for sale",
        f"Yes, you can still buy this item",
        f"Yes, it's available",
        f"This item hasn’t been sold yet",
        f"Still up for grabs!",
        f"Yes, it's on sale and available",
        f"It's currently available, let me know if you're interested"
        ]) 

    if any(word in user_input for word in shipping_keywords):
        return random.choice ([
        f"Sorry, shipping is not available\nPick-up is required",
        f"I can't offer delivery at the moment\nThis item is for local pickup only",
        f"Shipping is not an option for this item\nYou will need to pick it up",
        f"Unfortunately, I do not offer shipping\nThe item must be collected in person",
        f"No shipping available\nThe item can only be picked up from {location}",
        f"This item is only available for pickup\nNo delivery service is offered",
        f"I do not ship this item\nPlease arrange for a pickup",
        f"Pick-up only\nShipping is not available for this item"
        ])

    if any(word in user_input for word in accessories_keywords):
        return random.choice ([
        f"It comes with all original accessories",
        f"The package includes {accessories}",
        f"Yes, it includes {accessories}",
        f"Everything that came in the box is included",
        f"Accessories included: {accessories}",
        f"Comes with {accessories} as part of the package",
        f"Yes, {accessories} are part of the deal",
        f"You’ll receive {accessories} with this purchase"
        ])

    if any(word in user_input for word in location_keywords):
        return random.choice ([
        f"The item is available at {location}",
        f"You can pick it up from {location}",
        f"Meet-up is possible at {location}",
        f"Location: {location}",
        f"You can collect it at {location}",
        f"Pick-up point: {location}",
        f"We can arrange a meet-up at {location}",
        f"This item is located in {location}"
        ])

    if any(word in user_input for word in price_keywords):
        return random.choice ([
        f"The price is {price} Qar. Let me know if you’re interested!",
        f"It’s currently available for {price} Qar",
        f"I'm selling this for {price} Qar",
        f"The asking price is {price}",
        f"Price is set at {price} Qar",
        f"You can get this for {price} Qar",
        f"This item costs {price}",
        f"The listed price is {price}"
        ])

    if any(word in user_input for word in payment_keywords):
        return random.choice ([
        f"Payment is usually discussed on-site. Cash and local transactions are preferred",
        f"We accept cash and local payments.",
        f"Cash on pickup is preferred",
        f"Payment options can be discussed.",
        f"Payments can be made in person",
        f"Cash and standard payment methods accepted.",
        f"You can pay upon collection",
        f"We can talk about payment arrangements when you decide to buy"
        ])

    if any(word in user_input for word in guarantee_keywords):
        return random.choice ([
        f"This product comes with a {warranty_period} warranty", 
        f"A warranty of {warranty_period} is included",
        f"You get a {warranty_period} warranty with this item", 
        f"This item is covered under a {warranty_period} warranty",
        f"Warranty coverage lasts for {warranty_period}", 
        f"The product includes a {warranty_period} manufacturer warranty",
        f"You'll have a {warranty_period} guarantee on this", 
        f"Warranty period: {warranty_period}"
        ])

    if any(word in user_input for word in authenticity_keywords):
        return random.choice ([
        f"This is an original {brand} product. It comes with {authenticity_certificate}",
        f"Authenticity guaranteed: {brand} {title}.", "This is a genuine {brand} item",
        f"Yes, it's 100% authentic from {brand}.", "It has been verified as an original {brand} product",
        f"Comes with proof of authenticity: {authenticity_certificate}", 
        f"This is not a replica—it's an authentic {brand} item",
        f"You will receive an authenticity certificate: {authenticity_certificate}"
        ])

    if any(word in user_input for word in car_electronics_keywords):
        return random.choice ([
        f"It has {mileage} km and runs on {fuel_type}.",
        f"The battery life is around {battery_life}",
        f"This vehicle has {mileage} km on it",
        f"Fuel type: {fuel_type}",
        f"Battery condition: {battery_life}",
        f"It features a powerful {engine_capacity} engine",
        f"The mileage is {mileage}, and it's in good condition", 
        f"Runs efficiently with {fuel_type} and {battery_life} battery life"
        ])

    if any(word in user_input for word in visit_test_keywords):
        return random.choice ([
        f"You can visit to check and test it. Let’s schedule a time!", 
        f"A demo is possible, let me know when you want to visit",
        f"Feel free to come and test it",
        f"You are welcome to try before buying",
        f"Testing is allowed before purchase",
        f"We can arrange a time for you to see it working",
        f"I can show you how it works before you decide",
        f"Demo available upon request"
        ])

# ✅ GESTION DES PRIX ET NÉGOCIATIONS
def convert_price_format(price_str):
    """Convertit une offre de prix en valeur entière et demande confirmation si nécessaire"""

    if not price_str:
        return None  

    price_str = price_str.lower().replace("qar", "").replace(",", "").strip()
    price_str = price_str.replace(" ", "")  

    # Vérifier si c'est une année ou une heure pour éviter les erreurs
    if re.search(r'\b(202[0-9])\b', price_str) or re.search(r'\b(\d{1,2})\s?(am|pm)\b', price_str):
        return None  

    # ✅ Cas "5.8k", "6.2k" → Correction du format avec confirmation
    match = re.match(r'^(\d+)\.?(\d*)k$', price_str)  
    if match:
        thousands = int(match.group(1)) * 1000
        hundreds = int(match.group(2)[:1]) * 100 if match.group(2) else 0  
        final_price = thousands + hundreds
        return f"CONFIRMATION:{final_price}"  # Marque qu'on doit demander confirmation

    # ✅ Cas "5k8", "6k2" sans point
    match = re.match(r'^(\d+)k?(\d+)$', price_str)  
    if match:
        thousands = int(match.group(1)) * 1000
        hundreds = int(match.group(2)) * 100  
        return thousands + hundreds  

    # ✅ Capturer "5800", "6000", etc.
    match = re.match(r'^\d+$', price_str)
    if match:
        return int(match.group(0))  

    return None


def handle_price_negotiation(user_input, user_phone):
    """Gère la négociation des prix de manière plus humaine et engageante."""

    offer = convert_price_format(user_input)

    # 🔹 Si une confirmation est nécessaire
    if isinstance(offer, str) and "CONFIRMATION:" in offer:
        offer_amount = offer.replace("CONFIRMATION:", "")
        return random.choice([
            f"Did you mean {offer_amount} QAR?",
            f"I just want to make sure, you’re offering {offer_amount} QAR, right?",
            f"To be clear, are you suggesting {offer_amount} QAR?"
        ])

    if isinstance(offer, int):
        print(f"[DEBUG] Offre détectée: {offer} QAR")

        # 🔹 Si l'offre est très basse
        if offer < min_price * 0.9:
            return random.choice([
                "That offer is quite low. Maybe you'd like to come and see the product first?",
                "I respect all offers, but this one is too low. Are you open to adjusting your price?"
            ])

        # 🔹 Si l'offre est juste en dessous du prix mini
        elif offer < min_price:
            return random.choice([
                "That’s close! Let’s discuss this a bit more.",
                "We’re getting there! How about a slight adjustment?",
                "That’s a bit low. Could we meet somewhere in the middle?"
            ])

        # 🔹 Si l'offre atteint le prix minimum, demander confirmation
        elif offer == min_price:
            return random.choice([
                f"Okay, so {offer} QAR is your final offer?",
                f"Before we proceed, just to confirm, {offer} QAR is what you’re offering?",
                f"Alright! {offer} QAR seems fair. Just to finalize, this is your final price?"
            ])

        # 🔹 Si l'offre dépasse le prix minimum, accepter
        else:
            confirmed_deals[user_phone] = offer
            return "Alright! That works for me." + " " + propose_appointment_slots(user_phone)

    return "I'm not sure I understood your offer. Can you clarify?"


def propose_appointment_slots(user_phone):
    """Génère automatiquement les créneaux de rendez-vous pour finaliser un deal."""
    
    return f"""Here are the available slots:
    - Monday 10AM-12PM
    - Wednesday 3PM-5PM
    - Friday 6PM-8PM

    To confirm your visit, reply directly to this number:
    {seller_contact}
    Location: {location}
    Google Maps: {location_map_url}"""

def handle_location_request(user_input):
    """Fournit la localisation et le lien Google Maps"""

    location_requests = ["your location", "where are you", "where are you located", "what is your address", 
                         "pickup point", "meeting point", "where to meet", "how to find you"]

    # 🔍 Vérification Fuzzy
    best_match = process.extractOne(user_input, location_requests, scorer=fuzz.partial_ratio, score_cutoff=70)

    if best_match:
        return f"""Here’s the location for the product:
{location}
Google Maps: {location_map_url}
Contact for further details: {seller_contact}"""

    return None

# ✅ GESTION DES DEMANDES DE VISITE
def handle_visit_request(user_input, user_phone):
    """Gère les demandes de visite en vérifiant d’abord si l’acheteur est sérieux."""

    visit_requests = ["can i visit", "can i see", "can i come", "can i check", "can i pick up", "can i inspect"]
    if any(request in user_input for request in visit_requests):
        return f"""Before scheduling a visit, just a quick reminder: The price is {price} QAR.
        Are you seriously interested?"""

    confirmations = ["yes", "sure", "confirm", "alright", "let's do it"]
    if user_phone in pending_visits and user_input in confirmations:
        pending_visits.pop(user_phone)  
        return f"""Great! Your visit is confirmed. Here are the details:
        - Monday 10AM-12PM
        - Wednesday 3PM-5PM
        - Friday 6PM-8PM

        Location: {location}
        Google Maps: {location_map_url}
        Contact me if you need anything else: {seller_contact}"""

    return None


# ✅ GESTION DE LA LOCALISATION
def handle_location_request(user_input):
    """Fournit la localisation et le lien Google Maps"""

    location_requests = ["your location", "where are you", "where are you located", "what is your address", 
                         "pickup point", "meeting point", "where to meet", "how to find you"]

    # 🔍 Vérification Fuzzy
    best_match = process.extractOne(user_input, location_requests, scorer=fuzz.partial_ratio, score_cutoff=70)

    if best_match:
        return f"""Here’s the location for the product:
{location}
Google Maps: {location_map_url}
Contact for further details: {seller_contact}"""

    return None

# ✅ FONCTION PRINCIPALE DU CHATBOT
def handle_user_query(user_input, user_phone):
    """Gère toutes les interactions de manière logique et fluide."""

    user_input = clean_user_input(user_input)  # ✅ Nettoyage

    # ✅ Gestion des salutations
    greetings = ["hello", "hi", "hey", "salam", "bonjour", "good morning"]
    if user_input in greetings:
        return random.choice([
            "Hello! How can I help you?",
            "Salam! How can I assist you?",
            "Hey there! Need any details?",
            "Hello! Let me know if you have questions!"
        ])

    # ✅ Gestion des questions sur l’état du produit
    if any(word in user_input for word in ["is it new", "is it used", "condition", "state"]):
        return f"This product is in {condition} condition."

    # ✅ Gestion des questions sur le modèle
    if any(word in user_input for word in ["which model", "model", "version", "specs"]):
        return f"The model is {title}. It features {description}."

    # ✅ Gestion des questions sur l’année
    if any(word in user_input for word in ["which year", "year", "manufactured", "release date"]):
        return f"This product was manufactured in {year_model}."

    # ✅ Gestion des demandes de prix
    if any(word in user_input for word in ["how much", "price", "cost", "last price"]):
        return f"The price is {price} QAR. Let me know if you're interested!"

    # ✅ Gestion des demandes d’informations générales
    if any(word in user_input for word in ["information", "details", "tell me more"]):
        return random.choice([
            "Sure! Are you asking about the model, price, or condition?",
            "I can help! Do you need details about the specifications, price, or availability?",
            "Of course! Let me know what you're interested in: model, price, or something else?"
        ])

    # ✅ Gestion de la négociation des prix
    negotiation_response = handle_price_negotiation(user_input, user_phone)
    if negotiation_response:
        return negotiation_response

    # ✅ Vérifier si l'utilisateur demande une visite
    visit_response = handle_visit_request(user_input, user_phone)
    if visit_response:
        return visit_response

    # ✅ Gestion des demandes de localisation
    location_response = handle_location_request(user_input)
    if location_response:
        return location_response

    # ✅ Si rien n'est compris
    return random.choice([
        "Hmm, I didn’t quite get that. Could you clarify?",
        "Could you rephrase that?",
        "I'm not sure I understood. What do you mean?"
    ])
