import requests
import subprocess
import time
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

def get_ngrok_url():
    try:
        print("🚀 Lancement de Ngrok...")
        ngrok_process = subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                print(f"🌍 URL Ngrok trouvée : {tunnel['public_url']}")
                return tunnel["public_url"]
        print("❌ Aucune URL Ngrok détectée.")
        return None
    except Exception as e:
        print(f"❌ Erreur lors du lancement de Ngrok : {e}")
        return None

def get_twilio_number_sid():
    """ Récupère le SID du numéro Twilio enregistré """
    print("🔍 Vérification des numéros Twilio...")
    twilio_api_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/IncomingPhoneNumbers.json"
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    response = requests.get(twilio_api_url, auth=auth)
    if response.status_code != 200:
        print(f"❌ Erreur Twilio : {response.text}")
        return None

    phone_numbers = response.json()["incoming_phone_numbers"]
    for num in phone_numbers:
        print(f"📋 Numéro trouvé : {num['phone_number']} (SID: {num['sid']})")
        if num["phone_number"] == TWILIO_WHATSAPP_NUMBER:
            print(f"✅ Numéro WhatsApp Twilio identifié : {num['phone_number']}")
            return num["sid"]

    print(f"❌ Numéro WhatsApp Twilio introuvable ({TWILIO_WHATSAPP_NUMBER}). Vérifie ton compte Twilio.")
    return None

def update_twilio_webhook(ngrok_url):
    if not ngrok_url:
        print("❌ Impossible de mettre à jour Twilio car l'URL Ngrok est introuvable.")
        return

    webhook_url = f"{ngrok_url}/whatsapp"
    whatsapp_number_sid = get_twilio_number_sid()

    if not whatsapp_number_sid:
        print("❌ Aucun SID de numéro Twilio trouvé. Arrêt de la mise à jour.")
        return

    print(f"🔄 Mise à jour du Webhook Twilio avec {webhook_url}...")
    update_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/IncomingPhoneNumbers/{whatsapp_number_sid}.json"
    data = {"SmsUrl": webhook_url}

    response = requests.post(update_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), data=data)

    if response.status_code == 200:
        print(f"✅ Webhook Twilio mis à jour avec succès : {webhook_url}")
    else:
        print(f"❌ Erreur Twilio : {response.text}")

# 🚀 Exécution du script
ngrok_url = get_ngrok_url()
if ngrok_url:
    update_twilio_webhook(ngrok_url)
