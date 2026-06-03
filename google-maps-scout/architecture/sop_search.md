# SOP: Ricerca Business Google Maps
## Obiettivo
Trovare business in Ticino su Google Maps usando Places API Text Search.

## Input
- API Key (da .env)
- Lista query settoriali (rotazione per coprire tutti i settori)
- Regione: "Ticino, Svizzera"

## Logica
1. Esegui Text Search con query variata per settore (es. "negozio Bellinzona", "artigiano Locarno")
2. Per ogni risultato: estrai name, place_id, formatted_address, types
3. Filtra place_id già presenti in `memory/businesses_seen.json`
4. Per ogni nuovo business: chiama Place Details per ottenere website, phone, website
5. Tieni solo quelli con website=null o website da verificare
6. Accumula fino a raggiungere target (10 business validi)

## Query Template
```
["attività Lugano", "negozio Bellinzona", "artigiano Locarno", "ristorante Mendrisio",
 "parrucchiere Lugano", "studio Bellinzona", "officina Ticino", "estetista Locarno",
 "panetteria Ticino", "falegname Ticino", "idraulico Ticino", "elettricista Ticino"]
```

## Endpoint
- Text Search: `https://maps.googleapis.com/maps/api/place/textsearch/json`
- Place Details: `https://maps.googleapis.com/maps/api/place/details/json`
  - fields: `name,place_id,formatted_address,formatted_phone_number,website,types,editorial_summary`

## Casi Limite
- Quota esaurita: ferma e logga in progress.md
- 0 risultati per query: passa alla query successiva
- Tutti i risultati già visti: espandi con nuove query
