import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("marketplace.db")
cursor = conn.cursor()

# Vérification du contenu de la table listings
cursor.execute("SELECT id, title, category, price FROM listings")
listings = cursor.fetchall()

# Vérification du contenu
if not listings:
    print("❌ Aucune annonce trouvée dans la base de données !")
else:
    print("📌 Liste des annonces enregistrées :")
    for item in listings:
        print(f"🔹 {item[1]} - {item[2]} - {item[3]}")

# Fermer la connexion proprement
conn.close()
