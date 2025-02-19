import time
import random
import re
import unidecode
from twilio.rest import Client
from test_listing import title, category, description, price, location, min_price, seller_contact, image_url, available_slots, condition, year_model

# 🔴 Historique des échanges et confirmations
confirmed_deals = {}
scheduled_appointments = {}
user_conversations = {}

# ✅ Connexion à Twilio
twilio_client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")

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
    model_keywords = ["specs? detail", "which model", 
    "how much which type?", "tell me which type?", "whitch model", "wht which version", "why which specs? matter", 
    "model detail", "tell me which specs?", "what model detail", "which specs? detail", "which specs?", 
    "cnfiguration?", "tell me specs?", "which modl", 
    "prduct model?", "when what model happen", "when which specs? happen", "which type?", "why which type? matter", 
    "tell me model", "wht what model", 
    "which typ?", "wht model", "why which version matter", "yer what model", "yer which specs?", 
    "when technical details? happen", "whitch which specs?", "wht which model", "yer which specs?", 
    "how much which type?", "spcs?", 
    "model", "what abt which model", "whitch configuration?", "whitch which type?", "why which type? matter", 
    "technical detals?", "when product model? happen", "whitch which version", 
    "how much which version", "tell me which type?", "wht product model?", "why model matter", "why product model? matter", 
    "which type?", "whitch which version", 
    "model detail", "wat model", "whitch configuration?", "whitch technical details?", 
    "how much what model", "when model happen", "whitch configuration?", "yer which model", 
    "when which specs? happen", "which model", "wht what model", 
    "technical details?", "what abt model", 
    "product model? detail", "whitch technical details?", "wht product model?", "why product model? matter", "wich model", 
    "whitch which version", "wht which specs?", 
    "wht which model", "yer what model", 
    "prduct model?", "tell me which type?", "when product model? happen", 
    "what model", "yer which model", 
    "how much which type?", "tech details?", "when product model? happen", "which verion", "yer which model", 
    "cnfiguration?", "how much product model?", "tell me configuration?", "what abt model", "wht which model", 
    "prduct model?", "wht technical details?", 
    "model", "tell me what model", "whitch product model?", "why model matter", "yer which version", 
    "how much which specs?", "tell me configuration?", "whitch product model?", "whitch which type?", 
    "how much product model?", "tell me which version", "what model detail", "whitch model", 
    "what abt which version", "which model detail", "which model is it", "which model it is", "which specs? detail", "yer configuration?", 
    "tell me which type?", "when which specs? happen", "which type? detail", "wht model", "yer technical details?", 
    "how much which version", "what abt which type?", "which verion", 
    "when configuration? happen", "when what model happen", "whitch product model?", "whitch specs?", "why which version matter", 
    "model", "technical detals?", "what abt technical details?", 
    "how much what model", "yer which model", 
    "how much configuration?", "specs?", "tell me which specs?", 
    "wich model", "yer what model", "yer which type?", 
    "specs? detail", "tell me model", "tell me technical details?", "what abt what model", 
    "product modl?", "wat model", 
    "tech details?", "whitch which model", "wht what model", 
    "configuration?", "product model?", "tell me product model?", "wht which model", "yer configuration?", 
    "how much which model", "what abt configuration?", "what model detail", "which model detail", 
    "tell me which model", "which type? detail", "which verion", 
    "technical details? detail", "what model detail", "what model", "yer model", 
    "specs?", "tell me configuration?", "yer what model", "yer which version", 
    "tell me product model?", "which model detail", "yer model", "yer product model?", 
    "wht specs?", "yer which version", 
    "wht specs?", "wht which type?", 
    "how much configuration?", "spcs?", "when configuration? happen", "when which version happen", "yer which model", 
    "configuration?", "spcs?", "tell me which type?", "when which model happen", "why technical details? matter", 
    "cnfiguration?", "how much technical details?", "which type? detail", "whitch which specs?"]

    year_keywords = ["tell me what year", "what yer", "when which year happen", "why how old is it? matter", "year detail", 
    "model yer", "when year happen", "yer how old is it?", 
    "how much production year", "whitch how old is it?", "whitch model year", "year", "yer", 
    "what yer", "year", 
    "tell me which year", "what abt model year", "what yer", "yer model year", 
    "what abt what year", "yer production year", 
    "how old is it?", "yer", 
    "how much model year", "wich year", 
    "how old is it?", "tell me what year", "what abt what year", "when how old is it? happen", "year detail", 
    "wht release year", "year", "yer how old is it?", 
    "production year", "what abt how old is it?", "whitch year", "yer", 
    "whitch model year", "whitch what year", "yer which year", 
    "how old is it?", "what year", "which yer", "whitch model year", 
    "how much release year", "production yer", "whitch year", 
    "how oldd is it?", "tell me what year", "wht year", 
    "release year detail", "wht which year", "why how old is it? matter", 
    "how much model year", "why release year matter", "yer how old is it?", 
    "wht production year", "why what year matter", 
    "what abt model year", "what year detail", "when year happen", "which year", "whitch release year", 
    "tell me which year", "what abt year", "what year", "yer", 
    "when release year happen", "wht how old is it?", 
    "what abt what year", "whitch what year", 
    "how much how old is it?", "how old is it? detail", "how old is it?", "why how old is it? matter", "wich year", 
    "how much release year", "how old is it? detail", "tell me model year", "wht which year", 
    "production yer", "tell me release year", "why production year matter", "why year matter", "wich year", 
    "tell me release year", "what abt model year", "what yer", "why release year matter", "yer how old is it?", 
    "hw old is it?", "what abt year", "wht release year", "yer year", 
    "production year detail", "what year", "wht model year", "yer release year", 
    "what year", "when production year happen", "why year matter", 
    "when model year happen", "yer what year", 
    "how much how old is it?", "tell me how old is it?", "tell me model year", 
    "why model year matter", "year", "yer release year", 
    "how much production year", "whitch year", "wht how old is it?", 
    "how old is it?", "what abt release year", "wich year", "yer production year", 
    "how old is it?", "tell me model year", "which yer", "whitch model year", "yer which year", 
    "how much release year", "tell me how old is it?", 
    "what abt what year", "yer what year", 
    "how much production year", "what abt year", "whitch model year", "whitch which year", "wht release year", 
    "model yer", "whitch which year", "wht what year", "why year matter", 
    "what abt what year", "yer how old is it?", 
    "production yer", "relese year", "what yer", 
    "wat year", "what abt which year", 
    "tell me model year", "what year", "yer", 
    "production yer", "what abt release year", "year detail", 
    "when how old is it? happen", "wich year", 
    "when model year happen", "when release year happen", "when which year happen", "whitch year", "wht release year", 
    "prduction year", "tell me how old is it?", "tell me release year", "why which year matter", 
    "how much what year", "tell me year", "what abt which year", "why production year matter", "why which year matter", 
    "what abt release year", "what year", "when model year happen", 
    "production year detail", "what year detail", "what yer"]

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
    price_str = price_str.lower().replace("qar", "").replace(",", "").strip()
    if re.search(r'\b(202[0-9])\b', price_str) or re.search(r'\b(\d{1,2})\s?(am|pm)\b', price_str):
        return None  
    match = re.search(r'(\d+\.?\d*)k', price_str)
    if match:
        return int(float(match.group(1)) * 1000)
    match = re.search(r'\b\d+\b', price_str)
    if match:
        return int(match.group(0))
    return None

def handle_price_negotiation(user_input, user_phone):
    offer = convert_price_format(user_input)
    if offer is not None:
        if offer < min_price:
            return f"Sorry, {offer} QAR is too low. Looking for a better offer."
        else:
            confirmed_deals[user_phone] = offer
            return f"Deal confirmed at {offer} QAR. Please check my availability. " + propose_appointment_slots(user_phone)
    return None

# ✅ GESTION DES CRÉNEAUX ET RENDEZ-VOUS
def propose_appointment_slots(user_phone):
    if user_phone in scheduled_appointments:
        return None  
    slots_text = "\n".join([f"- {slot}" for slot in available_slots])
    message_body = (
        f"{slots_text}\n\n"
        f"To confirm your visit, reply directly to this number:\n"
        f"{seller_contact}\n"
        f"Location: {location}\n"
        f"Google Maps: https://maps.app.goo.gl/TzFqJmMTwx6iRoMG9"
    )
    return message_body

# ✅ GESTION DES DEMANDES DE VISITE
def handle_visit_request(user_input, user_phone):
    visit_keywords = ["visit", "pass", "can I check", "can I see", "can I take a look", "pick up", 
    "I want to collect", "can I pass by", "can I come", "can I visit", 
    "can I check it out", "where can I see it", "can I take a look before buying", 
    "can I test it", "can I hold it in my hands", "where is it available", 
    "can I drop by", "can I come over", "where to collect", "is it possible to check in person", 
    "is it available for viewing", "can I take a closer look", "can I come and see", 
    "can I come to your place", "where can I come", "is there a showroom", 
    "where can I pick it up", "is pick-up possible", "can I come and collect", 
    "do you offer pick-up", "do you allow pick-up", "where can I pick it up from", 
    "where do I have to go", "where do I need to come", "what is the location for pick-up",
    "can I inspect it", "can I see it in real life", "where are you located", 
    "can I check the condition in person", "where is the meet-up point", 
    "is meet-up possible", "where can we meet", "can I schedule a visit", 
    "can I arrange a meeting", "is it possible to come over", "can we meet for inspection",
    "can I verify the product", "where can I check it", "do you allow personal inspection",
    "can I come now", "can I pass by today", "can I drop by tomorrow", 
    "is there a time for pick-up", "is self-pickup possible", "where do you usually meet buyers",
    "can I come to check before deciding", "do you have a physical location", 
    "can I see it before paying", "can I try it before purchase", "can I hold it to see how it feels",
    "do you have a store", "is there a pick-up location", "where is your place",
    "how far are you", "can we arrange a meet-up", "do you meet buyers", "is it okay if I come",
    "is pick-up free", "do I need an appointment for pick-up", "can I check it out today",
    "is viewing available", "do you have a time for me to visit", "can I touch and feel it",
    "do you allow meet-ups", "do you meet customers", "do I need to book a time", 
    "can I drop by anytime", "do I need to bring anything for pick-up", "where is the collection point"]

    if any(word in user_input for word in visit_keywords):
        return f"Product: {title}\nPrice: {price}\n\nWould you like to choose a pick-up?"
    if user_input in ["yes", "interested", "i want to come", "i confirm"]:
        return propose_appointment_slots(user_phone)
    return None

# ✅ FONCTION PRINCIPALE DU CHATBOT
def handle_user_query(user_input, user_phone):
    user_input = unidecode.unidecode(user_input.strip().lower())
    user_conversations.setdefault(user_phone, []).append(user_input)
    return (
        handle_greetings(user_input) or
        handle_product_info(user_input) or
        handle_price_negotiation(user_input, user_phone) or
        handle_visit_request(user_input, user_phone) or
        random.choice(["I didn’t get that.", "Can you clarify?", "Sorry, what do you mean?", "Could you rephrase?", "Not sure I understood"])
    )
