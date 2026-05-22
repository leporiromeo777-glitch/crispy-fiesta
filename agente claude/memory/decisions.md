# Decisions — Scelte Architetturali

## D5 — Tre nuove regole di filtraggio (aggiunta 22/05/2026)
**Decisione**: Applicare tre regole aggiuntive che escludono business dal dataset.
1. **Solo email pubblica**: escluso chi non ha email trovata pubblicamente (Roberta Beauty Center, Ristorante Internazionale)
2. **No settore digitale**: escluso chi opera in marketing/IT/web agency (Onlinemarketpro, Manthea Sagl)
3. **No contatto senza consenso**: regola etica documentata — le email generate vanno inviate solo a chi ha reso pubblici i propri contatti
**Motivazione**: evitare spam, rispettare la privacy, e non contattare potenziali concorrenti.
**Effetto**: dataset ridotto da 10 a 6 business, tutti con email pubblica verificata.

---

## D1 — Firecrawl come motore principale (non Google API)
**Decisione**: Usare `firecrawl_search` come motore di ricerca principale invece di Google Custom Search API.
**Motivazione**: Firecrawl MCP è già attivo e connesso nella sessione. Evita di dover gestire credenziali Google API separate. Firecrawl_search restituisce già risultati web strutturati.
**Trade-off**: Meno controllo sul ranking geografico rispetto a Google, ma sufficiente per trovare 10 business.

## D2 — Gmail via link https://mail.google.com (non mailto:)
**Decisione**: Usare `https://mail.google.com/mail/?view=cm&...` invece di `mailto:`.
**Motivazione**: Il link Gmail apre direttamente l'interfaccia web di Gmail con i campi pre-compilati. Il mailto: dipende dal client email di sistema e potrebbe non aprire Gmail.
**Trade-off**: Richiede che l'utente sia loggato in Gmail nel browser.

## D3 — Output self-contained HTML (no framework)
**Decisione**: HTML + CSS inline, no dipendenze esterne (no Bootstrap, no CDN).
**Motivazione**: Il file deve funzionare offline e senza dipendenze. Massima portabilità.
**Trade-off**: CSS più verboso, ma zero rischi di breaking changes.

## D4 — Dati grezzi in /.tmp/ prima dell'HTML finale
**Decisione**: Salvare i dati JSON intermedi in `/.tmp/businesses_raw.json` prima di generare l'HTML.
**Motivazione**: Permette di rigenerare l'HTML senza ri-scrapare tutto. Utile per debug.
