# CLAUDE.md — Costituzione del Progetto
## Google Maps Scout — Routine Domenicale Ticino

---

## North Star
Ogni domenica alle 7:00, trovare automaticamente 10 business in Ticino **senza sito web o con sito broken/morto** tramite Google Maps API, e produrre un file HTML archiviato (`leads_YYYY-MM-DD.html`) con email pre-compilate Gmail per offerta Weblinkx. La routine ricorda i business già trovati e non li ripete.

---

## Schema Dati

### Input (fisso — eseguito da Zapier ogni domenica)
```json
{
  "region": "Ticino, Svizzera",
  "sectors": "tutti",
  "website_filter": "assente | broken | morto",
  "target_count": 10,
  "language": "it",
  "schedule": "domenica 07:00 CET"
}
```

### Business Record
```json
{
  "name": "string",
  "sector": "string",
  "address": "string",
  "city": "string (Ticino)",
  "phone": "string | null",
  "website": "string | null (se presente, verificato broken/morto)",
  "website_status": "assente | broken | morto | redirect_fail",
  "place_id": "string (Google Maps ID — chiave deduplicazione)",
  "email": "string | null",
  "description": "string (max 2 righe)",
  "email_subject": "string",
  "email_body": "string (max 100 parole, italiano)"
}
```

### Output Finale
```json
{
  "file": "output/leads_YYYY-MM-DD.html",
  "format": "HTML interattivo auto-contenuto con tabella filtrabile + badge stato sito",
  "email_action": "mailto: link che apre Gmail pre-compilato",
  "memory_update": "memory/businesses_seen.json aggiornato con i place_id già trovati"
}
```

---

## Regole Comportamentali

- **Lingua**: italiano in tutto
- **Mittente email**: Romeo Lepori — Weblinkx
- **Tono email**: amichevole ma professionale, max 100 parole
- **Offerta email**: creazione sito web + consulenza gratuita senza impegno
- **Chiusura email**: "ti/vi va di sentirci?" — MAI "facciamo una chiamata"
- **Settori target**: tutti i settori (no filtro settore)
- **Settori esclusi**: digitale / marketing / web agency / IT
- **Filtro sito**: includi business con website=null, o website che risponde con errore HTTP (4xx/5xx) o timeout
- **Deduplicazione**: ogni business è identificato dal `place_id` Google Maps; se già presente in `memory/businesses_seen.json`, viene saltato
- **Must-do**: includere solo business con almeno nome + città confermati
- **Must-not-do**: non inventare dati — se un campo non si trova, lasciarlo null
- **Must-not-do**: non includere business con sito web funzionante e attivo

---

## Stack Tecnologico

| Layer | Tool |
|-------|------|
| Scheduler | Zapier — Cron domenica 07:00 CET → webhook |
| Ricerca | Google Maps Places API (Nearby/Text Search) |
| Verifica sito | HTTP probe (requests + timeout 5s) |
| Output | File HTML statico auto-contenuto archiviato per data |
| Email | mailto: link → Gmail pre-compilato |
| Memoria | `memory/businesses_seen.json` (place_id già trovati) |

---

## Fasi B.L.A.S.T.

| Fase | Stato | Note |
|------|-------|------|
| B — Blueprint | ✅ | 5 domande discovery completate |
| L — Link | ⏳ | Verifica Google Maps API + Zapier |
| A — Architect | ⏳ | SOP ricerca, verifica sito, dedup, HTML |
| S — Stylize | ⏳ | Template HTML con badge stato sito |
| T — Trigger | ⏳ | Zapier webhook → script domenicale |

---

## Trigger

- **Tipo**: Zapier Schedule (cron) — ogni domenica alle 07:00 CET
- **Meccanismo**: Zapier chiama un webhook che esegue `execution/main.py`
- **Output**: file HTML salvato in `output/leads_YYYY-MM-DD.html`

---

## Invarianti Architetturali

1. Nessun dato inventato — solo ciò che è verificato via API/HTTP
2. Le credenziali vivono solo in `.env`
3. Tutti i dati grezzi passano per `/.tmp/` prima dell'output finale
4. Il file HTML è auto-contenuto (no dipendenze esterne CDN)
5. `place_id` Google Maps è la chiave universale di deduplicazione
6. Un business è incluso solo se website è null O la verifica HTTP fallisce
