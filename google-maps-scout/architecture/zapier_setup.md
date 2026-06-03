# Zapier Setup — Google Maps Scout
## Trigger domenicale automatico

### Zap da configurare

**Step 1 — Trigger: Schedule by Zapier**
- Trigger event: `Every Week`
- Day of week: `Sunday`
- Time of day: `7:00 AM`
- Timezone: `Europe/Zurich` (CET/CEST)

**Step 2 — Action: Webhooks by Zapier**
- Action event: `POST`
- URL: `http://<TUO_SERVER_IP>:8080/run`
- Payload type: `json`
- Body: `{"trigger": "zapier_schedule"}`

---

### Alternativa senza server (Code by Zapier)

Se non hai un server sempre attivo, usa **Code by Zapier (Python)**:

**Step 2 — Action: Code by Zapier**
- Action event: `Run Python`
- Incolla il contenuto di `execution/main.py` adattato per girare inline

---

### Note
- Il webhook deve essere raggiungibile pubblicamente (server VPS, Railway, Render, ecc.)
- Per test locali: usa ngrok (`ngrok http 8080`) per esporre il porta temporaneamente
- Credenziali: passa `GOOGLE_MAPS_API_KEY` come variabile ambiente sul server
