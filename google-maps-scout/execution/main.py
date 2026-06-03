#!/usr/bin/env python3
"""
Google Maps Scout — Routine domenicale Ticino
Trova 10 business senza sito web (o sito broken) e genera HTML archiviato.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import date
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / ".env"
MEMORY_FILE = BASE_DIR / "memory" / "businesses_seen.json"
OUTPUT_DIR = BASE_DIR / "output"
TMP_DIR = BASE_DIR / ".tmp"

OUTPUT_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

# --- Config ---
TARGET_COUNT = 10
EXCLUDED_TYPES = {"digital_marketing", "web_agency", "software_company", "internet_service_provider"}
QUERIES = [
    "ristorante Lugano Ticino",
    "negozio Bellinzona Ticino",
    "artigiano Locarno Ticino",
    "parrucchiere Lugano Ticino",
    "estetista Bellinzona Ticino",
    "officina Mendrisio Ticino",
    "panetteria Ticino Svizzera",
    "falegname Ticino Svizzera",
    "idraulico Lugano Ticino",
    "elettricista Bellinzona Ticino",
    "studio dentistico Ticino",
    "fioraio Ticino Svizzera",
    "bar caffè Lugano Ticino",
    "lavanderia Ticino Svizzera",
    "ottico Ticino Svizzera",
]


def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()


def load_seen_ids():
    if MEMORY_FILE.exists():
        try:
            return set(json.loads(MEMORY_FILE.read_text()).get("place_ids", []))
        except Exception:
            return set()
    return set()


def save_seen_ids(existing: set, new_ids: list):
    updated = list(existing | set(new_ids))
    MEMORY_FILE.write_text(json.dumps({"place_ids": updated}, indent=2))


def gmaps_get(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())


def text_search(query, api_key):
    params = urllib.parse.urlencode({"query": query, "key": api_key, "language": "it"})
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?{params}"
    data = gmaps_get(url)
    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        print(f"  [WARN] textsearch status: {data.get('status')} — {data.get('error_message','')}")
    return data.get("results", [])


def place_details(place_id, api_key):
    fields = "name,place_id,formatted_address,formatted_phone_number,website,types,editorial_summary"
    params = urllib.parse.urlencode({"place_id": place_id, "fields": fields, "key": api_key, "language": "it"})
    url = f"https://maps.googleapis.com/maps/api/place/details/json?{params}"
    data = gmaps_get(url)
    return data.get("result", {})


def check_website(url):
    if not url:
        return "assente"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            body = r.read(2000).decode("utf-8", errors="ignore").lower()
            if r.status >= 400:
                return "broken"
            parking_signals = ["domain for sale", "buy this domain", "parked domain", "coming soon", "under construction"]
            if any(s in body for s in parking_signals):
                return "parcheggiato"
            if len(body) < 500:
                return "quasi_vuoto"
            return "attivo"
    except urllib.error.HTTPError as e:
        return "broken" if e.code >= 400 else "morto"
    except Exception:
        return "morto"


def infer_sector(types):
    mapping = {
        "restaurant": "Ristorazione", "food": "Ristorazione", "bakery": "Panetteria",
        "bar": "Bar/Caffè", "cafe": "Bar/Caffè",
        "hair_care": "Parrucchiere", "beauty_salon": "Estetica", "spa": "Estetica",
        "dentist": "Studio Dentistico", "doctor": "Studio Medico", "lawyer": "Studio Legale",
        "accounting": "Commercialista", "insurance_agency": "Assicurazioni",
        "car_repair": "Officina Auto", "electrician": "Elettricista", "plumber": "Idraulico",
        "painter": "Pittore", "roofing_contractor": "Coperture",
        "florist": "Fioraio", "clothing_store": "Negozio Abbigliamento",
        "shoe_store": "Negozio Scarpe", "jewelry_store": "Gioielleria",
        "laundry": "Lavanderia", "dry_cleaning": "Lavanderia",
        "optician": "Ottico", "pharmacy": "Farmacia",
        "hardware_store": "Ferramenta", "furniture_store": "Arredamento",
        "general_contractor": "Artigiano", "carpenter": "Falegname",
    }
    for t in (types or []):
        if t in mapping:
            return mapping[t]
    return "Commercio locale"


def make_email(business):
    name = business["name"]
    sector = business["sector"]
    status = business["website_status"]

    if status == "assente":
        hook = f"Ho notato che {name} non ha ancora un sito web"
    elif status in ("morto", "broken"):
        hook = f"Ho notato che il sito di {name} sembra non essere raggiungibile"
    else:
        hook = f"Ho visto {name} su Google Maps"

    subject = f"Sito web per {name} — proposta gratuita"
    body = (
        f"Buongiorno,\n\n"
        f"{hook}. Sono Romeo Lepori di Weblinkx, creiamo siti web professionali "
        f"per piccole attività in Ticino.\n\n"
        f"Vi offriamo una consulenza gratuita e senza impegno per capire insieme "
        f"come un sito web moderno potrebbe aiutare {name} a farsi trovare online.\n\n"
        f"Ti/vi va di sentirci?\n\n"
        f"Romeo Lepori — Weblinkx"
    )
    return subject, body


def build_html(businesses, run_date):
    status_badge = {
        "assente": ('<span class="badge badge-absent">Senza sito</span>', "#e74c3c"),
        "morto": ('<span class="badge badge-dead">Sito morto</span>', "#c0392b"),
        "broken": ('<span class="badge badge-broken">Sito broken</span>', "#e67e22"),
        "parcheggiato": ('<span class="badge badge-parked">Parcheggiato</span>', "#f39c12"),
        "quasi_vuoto": ('<span class="badge badge-empty">Quasi vuoto</span>', "#95a5a6"),
    }

    rows = ""
    for b in businesses:
        badge_html, _ = status_badge.get(b["website_status"], ('<span class="badge">?</span>', "#999"))
        subject_enc = urllib.parse.quote(b["email_subject"])
        body_enc = urllib.parse.quote(b["email_body"])
        mailto = f"mailto:?subject={subject_enc}&body={body_enc}"

        phone_html = f'<a href="tel:{b["phone"]}">{b["phone"]}</a>' if b.get("phone") else "—"
        website_html = f'<a href="{b["website"]}" target="_blank">{b["website"][:40]}…</a>' if b.get("website") else "—"

        rows += f"""
        <tr>
          <td><strong>{b['name']}</strong></td>
          <td>{b['sector']}</td>
          <td>{b['city']}</td>
          <td>{phone_html}</td>
          <td>{website_html}</td>
          <td>{badge_html}</td>
          <td><a href="{mailto}" class="btn-gmail">✉ Gmail</a></td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Weblinkx Leads — {run_date}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f6fa; color: #2c3e50; }}
  header {{ background: #2c3e50; color: white; padding: 20px 32px; }}
  header h1 {{ font-size: 1.4rem; font-weight: 600; }}
  header p {{ font-size: 0.85rem; opacity: 0.7; margin-top: 4px; }}
  .container {{ padding: 24px 32px; }}
  .stats {{ display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
  .stat {{ background: white; border-radius: 8px; padding: 12px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .stat strong {{ display: block; font-size: 1.5rem; color: #e74c3c; }}
  .stat span {{ font-size: 0.8rem; color: #7f8c8d; }}
  .filter-bar {{ display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }}
  .filter-bar input {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 0.9rem; width: 220px; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
  th {{ background: #2c3e50; color: white; padding: 12px 14px; text-align: left; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }}
  td {{ padding: 11px 14px; border-bottom: 1px solid #f0f0f0; font-size: 0.88rem; vertical-align: middle; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #fafbfc; }}
  .badge {{ padding: 3px 9px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; color: white; }}
  .badge-absent {{ background: #e74c3c; }}
  .badge-dead {{ background: #c0392b; }}
  .badge-broken {{ background: #e67e22; }}
  .badge-parked {{ background: #f39c12; }}
  .badge-empty {{ background: #95a5a6; }}
  .btn-gmail {{ background: #4285f4; color: white; padding: 5px 12px; border-radius: 5px; text-decoration: none; font-size: 0.8rem; font-weight: 600; white-space: nowrap; }}
  .btn-gmail:hover {{ background: #3367d6; }}
  a {{ color: #3498db; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  footer {{ text-align: center; padding: 20px; font-size: 0.75rem; color: #bbb; }}
</style>
</head>
<body>
<header>
  <h1>Weblinkx — Lead Scout Google Maps</h1>
  <p>Generato domenica {run_date} · Ticino, Svizzera · Business senza sito web</p>
</header>
<div class="container">
  <div class="stats">
    <div class="stat"><strong>{len(businesses)}</strong><span>Lead trovati</span></div>
    <div class="stat"><strong>{sum(1 for b in businesses if b['website_status']=='assente')}</strong><span>Senza sito</span></div>
    <div class="stat"><strong>{sum(1 for b in businesses if b['website_status'] in ('morto','broken','parcheggiato'))}</strong><span>Sito non funzionante</span></div>
  </div>
  <div class="filter-bar">
    <input type="text" id="searchInput" placeholder="🔍 Filtra per nome, città, settore…" onkeyup="filterTable()">
  </div>
  <table id="leadsTable">
    <thead>
      <tr>
        <th>Nome</th><th>Settore</th><th>Città</th><th>Telefono</th><th>Sito attuale</th><th>Stato sito</th><th>Email</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>
<footer>Weblinkx · Romeo Lepori · Routine domenicale automatica</footer>
<script>
function filterTable() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  document.querySelectorAll('#leadsTable tbody tr').forEach(row => {{
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}
</script>
</body>
</html>"""


def main():
    load_env()
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("❌ GOOGLE_MAPS_API_KEY non trovata in .env")
        sys.exit(1)

    run_date = date.today().isoformat()
    print(f"🚀 Google Maps Scout — {run_date}")

    seen_ids = load_seen_ids()
    print(f"📋 Business già visti: {len(seen_ids)}")

    businesses = []
    tried_queries = 0

    for query in QUERIES:
        if len(businesses) >= TARGET_COUNT:
            break
        print(f"\n🔍 Query: {query}")
        tried_queries += 1
        try:
            results = text_search(query, api_key)
        except Exception as e:
            print(f"  [ERR] {e}")
            continue

        for r in results:
            if len(businesses) >= TARGET_COUNT:
                break
            pid = r.get("place_id")
            if not pid or pid in seen_ids:
                continue

            # Fetch details
            try:
                detail = place_details(pid, api_key)
                time.sleep(0.15)  # rate limit cortesia
            except Exception as e:
                print(f"  [ERR] details {pid}: {e}")
                continue

            website = detail.get("website")
            ws_status = check_website(website)

            if ws_status == "attivo":
                print(f"  ⏭ {detail.get('name')} — sito attivo, skip")
                continue

            addr = detail.get("formatted_address", "")
            city_parts = [p.strip() for p in addr.split(",")]
            city = city_parts[1] if len(city_parts) > 1 else city_parts[0]

            types = detail.get("types", [])
            sector = infer_sector(types)

            b = {
                "name": detail.get("name", r.get("name", "")),
                "sector": sector,
                "address": addr,
                "city": city,
                "phone": detail.get("formatted_phone_number"),
                "website": website,
                "website_status": ws_status,
                "place_id": pid,
            }
            b["email_subject"], b["email_body"] = make_email(b)
            businesses.append(b)
            seen_ids.add(pid)
            print(f"  ✅ {b['name']} ({city}) — {ws_status}")

    # Salva HTML
    html = build_html(businesses, run_date)
    out_file = OUTPUT_DIR / f"leads_{run_date}.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"\n✅ Output: {out_file}")

    # Aggiorna memoria
    save_seen_ids(load_seen_ids(), [b["place_id"] for b in businesses])
    print(f"💾 Memoria aggiornata — totale visti: {len(load_seen_ids())}")

    # Salva raw in .tmp
    raw_file = TMP_DIR / f"raw_{run_date}.json"
    raw_file.write_text(json.dumps(businesses, indent=2, ensure_ascii=False))

    print(f"\n🎯 Trovati {len(businesses)}/{TARGET_COUNT} business idonei in {tried_queries} query.")
    return out_file


if __name__ == "__main__":
    main()
