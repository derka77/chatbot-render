@echo off
title Démarrage Chatbot WhatsApp

:: Fermer Ngrok s'il est déjà en cours d'exécution
taskkill /IM ngrok.exe /F >nul 2>&1

:: Démarrer Flask dans une fenêtre PowerShell
echo 🚀 Démarrage du Chatbot Flask...
start powershell -NoExit -Command "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; python whatsapp_bot.py"

:: Attendre 5 secondes pour être sûr que Flask est démarré
timeout /t 5 /nobreak >nul

:: Mettre à jour automatiquement l'URL Webhook Twilio
echo 🔄 Mise à jour du Webhook Twilio...
powershell -NoExit -Command "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; python update_webhook.py"

:: Attendre 3 secondes pour être sûr que l'URL Webhook est mise à jour
timeout /t 3 /nobreak >nul

:: Lancer Ngrok dans PowerShell (sans ouvrir de fenêtre noire)
echo 🌍 Lancement de Ngrok...
powershell -NoExit -Command "cd C:\Users\KHADER.DESK-DCII000515\AppData\Roaming\Claude\CHATBOT; ngrok http 5000"

echo ✅ Tout est lancé ! Ouvre WhatsApp et teste.
exit
