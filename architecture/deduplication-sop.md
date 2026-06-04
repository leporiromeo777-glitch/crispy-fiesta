# SOP — Deduplicazione Attività Ticinesi

## Obiettivo
Evitare che la stessa attività appaia più volte nelle run successive di scraping Google Maps.

## Fonte della verità
`memory/seen_places.json` — file JSON committato nel repo, aggiornato ad ogni run.

## Identificatore univoco
Il `query_place_id` nell'URL Google Maps (es. `ChIJtTMORdU3hEcR9PauZTXR6PE`).
Fallback: nome normalizzato (lowercase, spazi → underscore) se il place_id non è disponibile.

## Destinazione finale
**Notion database:** https://app.notion.com/p/efdb49a8c6c74ec88800365fb38a3679
**Data Source ID:** `collection://9b588bbc-196e-424d-a695-d3eda442c6ec`

La tabella Notion è la fonte della verità. Il campo `Place ID` è la chiave di deduplicazione.

## Flusso per ogni nuova run

```
1. Apify scraper → /.tmp/raw_results.json
2. python3 execution/deduplicate.py \
       --input /.tmp/raw_results.json \
       --seen memory/seen_places.json \
       --output /.tmp/new_places.json
3. Leggi /.tmp/new_places.json → aggiungi righe al database Notion
   (notion-create-pages con data_source_id: 9b588bbc-196e-424d-a695-d3eda442c6ec)
4. git add memory/seen_places.json && git commit && git push
```

## Perché funziona a PC spento
Notion è cloud-based: le attività aggiunte persistono indipendentemente
dalla sessione Claude. Il registro seen_places.json nel repo GitHub
garantisce la deduplicazione tra run successive.

## Invarianti
- `seen_places.json` viene committato DOPO ogni run, mai prima
- Non cancellare voci dal registro (solo append)
- Se una run restituisce 0 nuove attività → espandere la query geografica o le categorie

## Aggiornamento manuale
Per aggiungere a mano una voce al registro:
```json
{
  "place_id": "ChIJ...",
  "name": "Nome Attività",
  "address": "Via ...",
  "added_on": "YYYY-MM-DD"
}
```
