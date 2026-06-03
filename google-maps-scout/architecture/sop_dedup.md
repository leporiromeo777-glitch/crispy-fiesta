# SOP: Deduplicazione
## Obiettivo
Non ripresentare mai un business già trovato in settimane precedenti.

## Meccanismo
- File: `memory/businesses_seen.json`
- Struttura: `{"place_ids": ["ChIJ...", ...]}`
- Prima di includere un business: controlla se place_id è nella lista
- Dopo generazione HTML: aggiungi i place_id dei 10 nuovi business alla lista

## Regole
- Mai rimuovere place_id dalla lista
- Il file cresce indefinitamente (è la memoria del sistema)
- In caso di file corrotto: ricrea con `{"place_ids": []}` e logga in progress.md
