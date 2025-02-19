# 📌 Configuration de l'annonce test pour le chatbot

# Titre de l'annonce
title = "MacBook Pro"

# Catégorie (Laptop, Car, Furniture, Smartphone...)
category = "Laptop"

# Marque du produit
brand = "Apple"

# Description détaillée
description = "Apple M1, 16GB RAM, 512GB SSD. Excellent condition. Rarely used, bought in 2023."

# 📌 Modèle et année
year_model = 2023  # Ajouté si absent

# Prix affiché sur l'annonce (en QAR)
price = 6500  # ✅ Correction de la syntaxe (Suppression du 'c')

# Prix minimum secret du vendeur (en QAR)
min_price = 6000  # ✅ Suppression de "QAR" pour éviter les erreurs de comparaison

# Localisation de l'objet
location = "Doha, The Pearl"

# 📌 Ajout du lien Google Maps
location_map_url = "https://maps.app.goo.gl/TzFqJmMTwx6iRoMG9"

# Contact du vendeur
seller_contact = "+97455667788"

# Lien image (optionnel)
image_url = "https://example.com/macbook-pro.jpg"

# ✅ Créneaux disponibles pour la visite
available_slots = [
    "Monday 10AM-12PM",
    "Wednesday 3PM-5PM",
    "Friday 6PM-8PM"
]

# ✅ État du produit (New/Used)
condition = "Used"  # Ou "New"

# ✅ Matériau (si applicable)
material = material if 'material' in locals() else None

# ✅ Dimensions (si applicable)
dimensions = dimensions if 'dimensions' in locals() else None

# ✅ Ajout de caractéristiques spécifiques selon la catégorie
if category == "Furniture":
    material = "Wood"  # Ex: Wood, Metal, Leather, Plastic...
    dimensions = "120x80x40 cm"  # Dimensions en cm
elif category == "Electronics":
    battery_life = None
    warranty = None
elif category == "Car":
    fuel_type = None
    mileage = None
elif category == "Clothing":
    size = None
    color = None
elif category == "Accessories":
    compatible_devices = None
    brand_compatibility = None
elif category == "Shipping":
    shipping_cost = None
    estimated_delivery = None

# ✅ Génération automatique des mots-clés pour faciliter la reconnaissance
tags = [brand, title, category] + description.split()[:5]  # Extraits de la description
