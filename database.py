import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("marketplace.db", check_same_thread=False)
cursor = conn.cursor()

# Vérifier si la table listings existe déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        price TEXT NOT NULL,
        location TEXT NOT NULL,
        availability TEXT NOT NULL,
        seller_contact TEXT NOT NULL,
        image_url TEXT,  -- URL de l'image
        min_price INTEGER DEFAULT 0  -- Prix minimum secret du vendeur
    )
''')
conn.commit()

def add_listing(title, category, description, price, location, availability, seller_contact, min_price, image_url=""):
    """Ajoute une nouvelle annonce avec un prix minimum secret"""
    cursor.execute('''
        INSERT INTO listings (title, category, description, price, location, availability, seller_contact, min_price, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, category, description, price, location, availability, seller_contact, min_price, image_url))
    conn.commit()

def search_listing(category=None, title=None):
    """Recherche des annonces par catégorie et/ou titre"""
    query = "SELECT * FROM listings WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    cursor.execute(query, params)
    return cursor.fetchall()

# Ajout d'annonces fictives avec `min_price`
def add_sample_listings():
    add_listing("Toyota Corolla 2018", "Car", "Automatic, well-maintained, low mileage.",
                "QAR 40,000", "Doha, Qatar", "Available now", "+97412345678", 38000,
                "https://example.com/toyota-corolla.jpg")

    add_listing("IKEA Sofa Set", "Furniture", "Comfortable 3-seater, like new.",
                "QAR 1,500", "Al Wakrah, Qatar", "Available now", "+97487654321", 1300,
                "https://example.com/ikea-sofa.jpg")

    add_listing("PlayStation 5", "Electronics", "Brand new, sealed in box, 825GB storage.",
                "QAR 2,300", "Doha, Qatar", "Available now", "+97411223344", 2100,
                "https://example.com/ps5.jpg")

    add_listing("iPhone 14 Pro Max", "Smartphone", "128GB, Deep Purple, in excellent condition.",
                "QAR 4,500", "Doha, Qatar", "Available now", "+97455667788", 4200,
                "https://example.com/iphone14.jpg")

    add_listing("LG Smart TV 55’", "Electronics", "4K UHD, AI ThinQ, excellent condition.",
                "QAR 2,000", "Al Rayyan, Qatar", "Available now", "+97444332211", 1800,
                "https://example.com/lg-tv.jpg")

    print("✅ Annonces fictives ajoutées avec succès !")

# Ajouter les annonces fictives si nécessaire
add_sample_listings()
