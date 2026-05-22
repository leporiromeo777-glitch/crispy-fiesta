# Task Plan — Weblinkx Business Scout

## Obiettivo
10 business ticinesi (max 30 dipendenti) → HTML interattivo con email pronte per Gmail.

---

## Fasi e Checklist

### FASE B — Blueprint ✅
- [x] North Star definita
- [x] Integrazioni identificate (Google, Firecrawl, Gmail)
- [x] Schema dati definito in CLAUDE.md
- [x] Regole comportamentali definite

### FASE L — Link ⏳
- [ ] Verifica Google Custom Search API (chiave + CSE ID)
- [ ] Verifica Firecrawl MCP (connessione attiva)
- [ ] Test probe: 1 ricerca Google → risultati
- [ ] Test probe: 1 scrape Firecrawl → contenuto

### FASE A — Architect ⏳
- [ ] SOP: ricerca business (`architecture/sop_search.md`)
- [ ] SOP: arricchimento dati (`architecture/sop_enrich.md`)
- [ ] SOP: generazione email (`architecture/sop_email.md`)
- [ ] SOP: generazione HTML (`architecture/sop_html.md`)

### FASE S — Stylize ⏳
- [ ] Template HTML con tabella interattiva
- [ ] Stile CSS pulito e responsivo
- [ ] Pulsante "Apri in Gmail" funzionante
- [ ] Verifica mailto: link con parametri pre-compilati

### FASE T — Trigger ⏳
- [ ] Script main.py funzionante end-to-end
- [ ] Output HTML verificato in browser
- [ ] Documentazione finale in CLAUDE.md

---

## Vincoli
- Max 10 aziende
- Max 30 dipendenti per azienda
- Solo Ticino (Svizzera)
- Email max 100 parole, italiano
