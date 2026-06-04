# ROUTINE — Scraping Attività Ticinesi Senza Sito Web

## Contesto
Sei un agente automatico. Stai girando su GitHub Actions, senza supervisione umana.
Il tuo compito è trovare nuove attività ticinesi senza sito web su Google Maps,
filtrarle dai duplicati già visti, e aggiungerle al database Notion.

Non chiedere conferme. Non fermarti a metà. Completa tutte le fasi in sequenza.

---

## FASE 1 — Leggi il registro dei duplicati

Leggi il file `memory/seen_places.json`.
Estrai tutti i `place_id` già presenti — questi non devono mai uscire di nuovo.

---

## FASE 2 — Scraping Google Maps via Apify (Zapier)

Usa il tool Zapier con l'app Apify (`ApifyCLIAPI`) per lanciare l'actor
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
- Attendi almeno 60 secondi (usa un loop di fetch finché il dataset non è popolato)
- Recupera i risultati con `fetchDatasetItems`

Raccogli tutti i risultati in una lista unica.

---

## FASE 3 — Deduplicazione

Per ogni attività raccolta nella Fase 2:

1. Estrai il `place_id` dall'URL Google Maps nel campo `mapsUrl`
   (il valore dopo `query_place_id=`)
2. Se il `place_id` è già in `memory/seen_places.json` → **scarta** l'attività
3. Se è nuovo → **tienila** e aggiungila alla lista delle nuove attività

Se la lista delle nuove attività è vuota:
- Scrivi in `memory/progress.md` la data e "Nessuna nuova attività trovata"
- Committa e pusha
- **Termina**

---

## FASE 4 — Aggiungi le nuove attività al database Notion

**Database Notion:** `https://app.notion.com/p/efdb49a8c6c74ec88800365fb38a3679`
**Data Source ID:** `9b588bbc-196e-424d-a695-d3eda442c6ec`

Per ogni nuova attività, crea una pagina nel database Notion con questi campi:

| Campo Notion     | Fonte dato Apify              |
|------------------|-------------------------------|
| `Nome`           | `name`                        |
| `Categoria`      | `categoryName` (mappa sotto)  |
| `Città`          | `city` (mappa sotto)          |
| `Indirizzo`      | `address`                     |
| `Telefono`       | `phoneUnformatted`            |
| `Rating`         | `totalScore`                  |
| `Recensioni`     | `reviewsCount`                |
| `Google Maps`    | `mapsUrl`                     |
| `Place ID`       | estratto da `mapsUrl`         |
| `Data aggiunta`  | data odierna (YYYY-MM-DD)     |

**Mappatura Categoria** (se non corrisponde, usa "Altro"):
- restaurant / ristorante → `Ristorante`
- bar → `Bar`
- cafe / caffè → `Caffè`
- snack bar → `Snack Bar`
- family restaurant → `Ristorante Familiare`
- store / shop / negozio → `Negozio`
- artisan / artigiano → `Artigiano`

**Mappatura Città** (se non corrisponde, usa "Altro"):
- Lugano / Viganello / Breganzona / Massagno → `Lugano`
- Bellinzona → `Bellinzona`
- Locarno / Ascona / Muralto → `Locarno`
- Mendrisio / Chiasso / Lugano → `Mendrisio`

---

## FASE 5 — Aggiorna il registro dei duplicati

Apri `memory/seen_places.json` e aggiungi ogni nuova attività alla lista `places`:

```json
{
  "place_id": "<place_id estratto>",
  "name": "<nome attività>",
  "address": "<indirizzo>",
  "added_on": "<data odierna YYYY-MM-DD>"
}
```

Aggiorna anche il campo `"last_updated"` con la data odierna.

---

## FASE 6 — Aggiorna il log di progresso

Apri `memory/progress.md` e aggiungi in cima una riga con:

```
## Run YYYY-MM-DD
- Query eseguite: [lista query]
- Risultati totali Apify: N
- Duplicati scartati: N
- Nuove attività aggiunte a Notion: N
- Errori: nessuno / [descrizione se presenti]
```

---

## FASE 7 — Commit e Push

Committa e pusha sul branch `claude/bold-lovelace-ATxWh` con questo messaggio:

```
chore(routine): add N new Ticino activities — YYYY-MM-DD

- Queries: [lista query usate]
- New: N | Duplicates skipped: N
- Notion DB updated
```

---

## Regole operative

1. **Non fermarti mai a metà** — se una query Apify fallisce, logga l'errore in `progress.md` e continua con la prossima
2. **Non aggiungere duplicati** — il `place_id` è la chiave assoluta
3. **Non inventare dati** — se un campo è null in Apify, lascialo null in Notion
4. **Priorità alla stabilità** — meglio 3 attività corrette che 10 con dati inventati
5. **Sempre committa** — anche se non ci sono nuove attività, aggiorna `progress.md` e committa
