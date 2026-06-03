# SOP: Generazione HTML
## Obiettivo
Produrre un file HTML auto-contenuto archiviato per data.

## Struttura Output
- Path: `output/leads_YYYY-MM-DD.html`
- Auto-contenuto: CSS inline, no CDN
- Tabella filtrabile via JS vanilla
- Badge colorati per stato sito (assente/broken/morto/parcheggiato/quasi_vuoto)
- Pulsante Gmail: `mailto:?subject=...&body=...` URL-encoded

## Campi Tabella
Nome | Settore | Città | Telefono | Sito attuale | Stato sito | Email (btn Gmail)

## Badge Colori
- assente → rosso #e74c3c
- morto → rosso scuro #c0392b
- broken → arancione #e67e22
- parcheggiato → giallo #f39c12
- quasi_vuoto → grigio #95a5a6
