# Findings — Ricerca e Scoperte

## Firecrawl MCP
- MCP attivo e rilevato nella sessione corrente
- Tool disponibili: firecrawl_search, firecrawl_scrape, firecrawl_extract, firecrawl_crawl, firecrawl_map
- `firecrawl_search` può fare ricerche web direttamente (alternativa a Google API)
- `firecrawl_extract` può estrarre dati strutturati da una pagina con schema JSON

## Apify
- Disponibile come MCP alternativo per scraping
- Ha attori per LinkedIn, Google Maps, social media
- Da valutare per arricchimento dati social se Firecrawl non basta

## Strategia di Ricerca Business Ticino
- Query efficaci: "piccole imprese Ticino", "aziende Lugano", "negozi Bellinzona", "artigiani Locarno"
- Fonti primarie da scrapare:
  - Google Maps / Google My Business
  - Pagine Gialle Svizzera (local.ch, search.ch)
  - LinkedIn aziende
  - Siti web aziendali
- Stima dipendenti: ricavabile da LinkedIn "About" o sito web sezione "Team"

## Note Tecniche
- Il mailto: link supporta `to`, `subject`, `body` come parametri URL-encoded
- Per aprire Gmail specificamente: `https://mail.google.com/mail/?view=cm&to=EMAIL&su=SUBJECT&body=BODY`
- Il file HTML sarà self-contained (CSS inline, no CDN)
