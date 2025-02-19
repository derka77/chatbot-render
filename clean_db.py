import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("marketplace.db")
cursor = conn.cursor()

# Suppression des doublons en gardant seulement une copie
cursor.execute("""
    DELETE FROM listings
    WHERE id NOT IN (
        SELECT MIN(id) FROM listings GROUP BY title, category, price, location
    )
""")
conn.commit()

print("✅ Doublons supprimés avec succès !")

# Vérification après nettoyage
cursor.execute("SELECT id, title, category, price FROM listings")
listings = cursor.fetchall()

print("📌 Liste des annonces après nettoyage :")
for item in listings:
    print(f"🔹 {item[1]} - {item[2]} - {item[3]}")

# Fermer la connexion
conn.close()
