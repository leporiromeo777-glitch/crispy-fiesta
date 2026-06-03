# SOP: Verifica Sito Web Broken/Morto
## Obiettivo
Determinare se un sito web è assente, broken o morto.

## Logica
1. Se `website` è null/vuoto → stato = "assente" → includi
2. Se website presente → HTTP GET con timeout 5s
   - ConnectionError / Timeout → stato = "morto"
   - Status >= 400 → stato = "broken"
   - Redirect a pagina parcheggio dominio (body contiene "domain for sale", "buy this domain", "parked") → stato = "parcheggiato"
   - Status 200 ma body < 500 chars → stato = "quasi vuoto"
   - Status 200, body normale → ESCLUDI (sito funzionante)

## Headers da usare
```python
headers = {"User-Agent": "Mozilla/5.0 (compatible; bot/1.0)"}
```

## Output per ogni business
```json
{"website_status": "assente | morto | broken | parcheggiato | quasi_vuoto"}
```
