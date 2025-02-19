# Script pour lancer Flask, mettre à jour Twilio Webhook et lancer Ngrok automatiquement

# 📌 Ouvrir une première fenêtre PowerShell pour Flask
Start-Process powershell -ArgumentList "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; python whatsapp_bot.py"

# ⏳ Attendre 5 secondes pour être sûr que Flask est démarré
Start-Sleep -Seconds 5

# 📌 Mettre à jour automatiquement l'URL Webhook Twilio
Start-Process powershell -ArgumentList "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; python update_webhook.py"

# ⏳ Attendre 3 secondes pour être sûr que l'URL Webhook est mise à jour
Start-Sleep -Seconds 3

# 📌 Ouvrir une deuxième fenêtre PowerShell pour Ngrok
Start-Process powershell -ArgumentList "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; ngrok http 5000"
