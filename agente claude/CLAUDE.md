# CLAUDE.md — Costituzione del Progetto
## Weblinkx Lead Scout

---

## North Star (v2)
Trovare 10 piccoli business locali in Ticino (max 30 dipendenti, settori: ristorazione, estetica, studi professionali, negozi locali, artigiani), arricchire i dati via scraping, e produrre **`weblinkx_leads.html`** — tabella HTML interattiva con email personalizzate per settore che offrono creazione sito web + consulenza gratuita.

---

## Schema Dati

### Input
```json
{
  "query": "piccole aziende Ticino settori locali",
  "region": "Ticino, Svizzera",
  "max_employees": 30,
  "target_count": 10,
  "language": "it",
  "sectors": ["ristorazione", "parrucchieri/estetisti", "studi dentistici/professionali", "negozi locali", "artigiani"]
}
```

### Business Record (per ogni azienda trovata)
```json
{
  "name": "string",
  "sector": "string",
  "address": "string",
  "city": "string (Ticino)",
  "phone": "string | null",
  "email": "string | null",
  "website": "string | null",
  "employees_estimate": "string (es. '5-10')",
  "description": "string (max 2 righe)",
  "site_quality": "In costruzione | Quasi assente | Datato | Basilare | Moderno",
  "email_subject": "string",
  "email_body": "string (max 100 parole, italiano)"
}
```

### Output Finale
```json
{
  "file": "weblinkx_leads.html",
  "format": "HTML interattivo con tabella filtrabile + badge qualità sito",
  "email_action": "mailto: link che apre Gmail pre-compilato"
}
```

---

## Regole Comportamentali

- **Lingua**: italiano in tutto
- **Mittente email**: Romeo Lepori — Weblinkx
- **Tono email**: amichevole ma professionale, max 100 parole
- **Offerta email**: creazione sito web + consulenza gratuita senza impegno
- **Chiusura email**: "ti/vi va di sentirci?" — MAI "facciamo una chiamata"
- **Settori target**: ristorazione, parrucchieri, studi professionali, negozi locali, artigiani
- **Settori esclusi**: digitale / marketing / web agency / IT
- **Dipendenti**: max 30 (stimati da web, non verificati ufficialmente)
- **Filtro sito**: priorità a siti assenti, in costruzione o datati
- **Must-do**: includere solo business con almeno nome + città confermati
- **Must-do**: includere solo attività con email pubblica verificata
- **Must-not-do**: non inventare dati — se un campo non si trova, lasciarlo null
- **Must-not-do**: non includere business già presenti in `/memory/businesses_contacted.md`
- **Valutazione sito**: criteri autonomi (no HTTPS, no mobile, design pre-2015, sito in costruzione, sito quasi vuoto)

---

## Stack Tecnologico

| Layer | Tool |
|-------|------|
| Ricerca | Chrome MCP (Google Search) — fallback da Firecrawl MCP |
| Scraping | Chrome MCP / Firecrawl MCP |
| Output | File HTML statico auto-contenuto |
| Email | mailto: link → Gmail |

---

## Fasi B.L.A.S.T.

| Fase | Stato | Note |
|------|-------|------|
| B — Blueprint | ✅ v2 | 5 domande discovery, schema confermato |
| L — Link | ✅ | Chrome MCP operativo (Firecrawl esaurito) |
| A — Architect | ✅ | Ricerca per settore + verifica sito qualità |
| S — Stylize | ✅ | weblinkx_leads.html generato con badge qualità sito |
| T — Trigger | ✅ | File consegnato in root progetto |

---

## Output Consegnati

| File | Descrizione |
|------|-------------|
| `ticino_businesses.html` | v1 — 6 business, maggio 2026 |
| `weblinkx_leads.html` | v2 — 10 business, focus siti datati/assenti, maggio 2026 |

---

## Invarianti Architetturali

1. Nessun dato inventato — solo ciò che è verificato via scraping/ricerca web
2. Le credenziali vivono solo in `.env`
3. Tutti i dati grezzi passano per `/.tmp/` prima dell'output finale
4. Il file HTML è auto-contenuto (no dipendenze esterne)
5. Nessun business già presente in `businesses_contacted.md` va incluso
