# Decisions — Google Maps Scout

## D1 — Google Maps API vs Firecrawl per ricerca business
**Scelta**: Google Maps Places API  
**Motivazione**: restituisce direttamente il campo `website` (o la sua assenza), il `place_id` per deduplicazione, e dati strutturati (nome, indirizzo, telefono, settore). Firecrawl richiederebbe scraping HTML non strutturato di Google Maps, fragile e soggetto a ban.

## D2 — place_id come chiave di deduplicazione
**Scelta**: `place_id` Google Maps  
**Motivazione**: è l'identificatore stabile e univoco di Google per ogni attività. Più affidabile di nome+indirizzo (che possono variare in formato). Viene salvato in `memory/businesses_seen.json`.

## D3 — Verifica sito broken via HTTP probe
**Scelta**: `requests.get(url, timeout=5)` con catch su errori  
**Motivazione**: semplice, deterministico, senza dipendenze esterne. Un sito è considerato morto se: timeout, ConnectionError, status >= 400, o redirect a pagina di parcheggio dominio.

## D4 — Output archiviato per data (non sovrascritto)
**Scelta**: `output/leads_YYYY-MM-DD.html`  
**Motivazione**: richiesta esplicita dell'utente. Permette storico settimanale e confronto nel tempo.

## D5 — Zapier come scheduler
**Scelta**: Zapier Schedule → Webhooks/Code  
**Motivazione**: già disponibile nell'ambiente, no infrastruttura aggiuntiva, configurabile in pochi minuti.
