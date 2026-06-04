# ROUTINE — Scraping Attività Ticinesi Senza Sito Web

## Contesto
Sei un agente automatico che gira su Claude, senza supervisione umana.
Il tuo compito è trovare nuove attività ticinesi senza sito web su Google Maps,
filtrarle dai duplicati già presenti in Notion, e aggiungere solo le nuove.

Non chiedere conferme. Non fermarti a metà. Completa tutte le fasi in sequenza.

---

## FASE 1 — Leggi i duplicati da Notion

Cerca nel database Notion **"Attività Ticinesi — Senza Sito Web"**
(`https://app.notion.com/p/efdb49a8c6c74ec88800365fb38a3679`)
e recupera tutti i valori del campo **`Place ID`** già presenti.

Costruisci una lista di Place ID da escludere nelle fasi successive.

---

## FASE 2 — Scraping Google Maps via Apify (Zapier)

Usa Zapier con l'app Apify (`ApifyCLIAPI`) per lanciare l'actor
`compass/crawler-google-places` con questi parametri:

- **Filtro sito web:** solo attività SENZA sito web (`withoutWebsite`)
- **Lingua:** italiano (`it`)
- **Paese:** Svizzera (`CH`)
- **Limite per query:** 20 risultati

Esegui le seguenti query **in sequenza**, una run Apify per ognuna:

1. `ristorante, Lugano, Ticino, Switzerland`
2. `bar, Bellinzona, Ticino, Switzerland`
3. `negozio, Locarno, Ticino, Switzerland`
4. `artigiano, Mendrisio, Ticino, Switzerland`
5. `caffè, Lugano, Ticino, Switzerland`

Per ogni run:
- Avvia l'actor con `createActorRun` (runSync: no)
- Usa un loop di `fetchDatasetItems` finché il dataset non è popolato
- Raccogli tutti i risultati in una lista unica

---

## FASE 3 — Deduplicazione

Per ogni attività raccolta nella Fase 2:

1. Estrai il `place_id` dall'URL nel campo `mapsUrl`
   (il valore dopo `query_place_id=`)
2. Se il `place_id` è già nella lista della Fase 1 → **scarta**
3. Se è nuovo → **tienila**

Se non ci sono nuove attività → **termina** senza fare altro.

---

## FASE 4 — Aggiungi le nuove attività al database Notion

**Data Source ID:** `9b588bbc-196e-424d-a695-d3eda442c6ec`

Per ogni nuova attività crea una pagina Notion con questi campi:

| Campo Notion    | Fonte dato Apify                      |
|-----------------|---------------------------------------|
| `Nome`          | `name`                                |
| `Categoria`     | `categoryName` (mappa sotto)          |
| `Città`         | estratta dall'indirizzo (mappa sotto) |
| `Indirizzo`     | `address`                             |
| `Telefono`      | `phoneUnformatted`                    |
| `Rating`        | `totalScore`                          |
| `Recensioni`    | `reviewsCount`                        |
| `Google Maps`   | `mapsUrl`                             |
| `Place ID`      | estratto da `mapsUrl`                 |
| `Data aggiunta` | data odierna (YYYY-MM-DD)             |

**Mappatura Categoria** (default: `Altro`):
- restaurant / ristorante → `Ristorante`
- bar → `Bar`
- cafe / caffè → `Caffè`
- snack bar → `Snack Bar`
- family restaurant → `Ristorante Familiare`
- store / shop / negozio → `Negozio`
- artisan / artigiano → `Artigiano`

**Mappatura Città** (default: `Altro`):
- Lugano / Viganello / Breganzona / Massagno → `Lugano`
- Bellinzona → `Bellinzona`
- Locarno / Ascona / Muralto → `Locarno`
- Mendrisio / Chiasso → `Mendrisio`

---

## Regole operative

1. **Non fermarti mai a metà** — se una query Apify fallisce, continua con la prossima
2. **Non aggiungere duplicati** — il `place_id` è la chiave assoluta
3. **Non inventare dati** — se un campo è null in Apify, lascialo null in Notion
4. **Priorità alla stabilità** — meglio 3 attività corrette che 10 con dati inventati
