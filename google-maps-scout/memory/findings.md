# Findings — Google Maps Scout

## Progetto Esistente (Weblinkx Lead Scout)
- Struttura: ricerca manuale → HTML statico con mailto Gmail
- Stack: Firecrawl MCP + Chrome MCP per scraping
- Output: `weblinkx_leads.html` (run manuale, non schedulato)
- Schema business: name, sector, address, city, phone, email, website, site_quality, email_body

## Differenze Nuova Routine
- Trigger: automatico Zapier domenica 07:00 CET (vs manuale)
- Fonte dati: Google Maps Places API (vs ricerca web generica)
- Filtro: website=null OR HTTP broken (vs qualità sito datata)
- Output: archiviato per data (vs file singolo sovrascritto)
- Memoria: deduplicazione via place_id (vs nessuna)
- Settori: tutti (vs ristorazione/parrucchieri/studi/artigiani)

## Google Maps Places API — Note Tecniche
- Endpoint rilevante: Text Search / Nearby Search
- Campo website: disponibile nella risposta Place Details
- place_id: identificatore univoco stabile per deduplicazione
- Limite gratuito: 200$/mese crediti; Text Search ~0.032$/request
- Verifica sito broken: requests.get(url, timeout=5) → catch ConnectionError, HTTPError, Timeout

## Zapier — Meccanismo
- Trigger: Schedule by Zapier (ogni settimana, domenica)
- Action: Webhooks by Zapier (POST a endpoint) oppure Code by Zapier (Python)
- Alternativa: Zapier → GitHub Actions dispatch
