# Task Plan — Google Maps Scout (Domenicale Ticino)

## Obiettivo
Routine automatica domenicale: 10 business Ticino senza sito web / sito morto → HTML archiviato con email Gmail pre-compilate.

---

## Fasi e Checklist

### FASE B — Blueprint ✅
- [x] North Star definita
- [x] Integrazioni: Zapier + Google Maps API + HTML
- [x] Fonte verità: ricerca fissa tutto Ticino, tutti settori
- [x] Payload: file archiviato `leads_YYYY-MM-DD.html`
- [x] Regole: broken inclusi, 10 risultati, email precompilata, deduplicazione

### FASE L — Link ⏳
- [ ] Verifica Google Maps Places API (chiave in .env)
- [ ] Test probe: 1 ricerca Places API → risultati Ticino
- [ ] Test probe: verifica HTTP sito → broken/morto rilevato
- [ ] Verifica Zapier: webhook attivabile

### FASE A — Architect ⏳
- [ ] SOP: ricerca Google Maps (`architecture/sop_search.md`)
- [ ] SOP: verifica sito broken (`architecture/sop_verify_site.md`)
- [ ] SOP: deduplicazione (`architecture/sop_dedup.md`)
- [ ] SOP: generazione HTML (`architecture/sop_html.md`)

### FASE S — Stylize ⏳
- [ ] Template HTML con badge stato sito (assente/broken/morto)
- [ ] Tabella filtrabile, stile pulito
- [ ] Pulsante "Apri in Gmail" funzionante

### FASE T — Trigger ⏳
- [ ] `execution/main.py` funzionante end-to-end
- [ ] Zapier Schedule configurato (domenica 07:00 CET)
- [ ] Output HTML verificato in browser
- [ ] Documentazione finale in CLAUDE.md
