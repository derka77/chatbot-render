from dotenv import load_dotenv
import os

# Charger .env
load_dotenv()

# Vérifier si les variables sont bien chargées
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("TWILIO_ACCOUNT_SID:", os.getenv("TWILIO_ACCOUNT_SID"))
print("TWILIO_AUTH_TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
