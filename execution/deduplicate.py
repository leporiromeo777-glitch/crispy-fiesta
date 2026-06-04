#!/usr/bin/env python3
"""
Deduplication engine per le attività ticinesi.

Uso:
  python3 execution/deduplicate.py --input /.tmp/raw_results.json
                                   --seen memory/seen_places.json
                                   --output /.tmp/new_places.json

Legge i risultati grezzi di Apify, filtra i place_id già visti,
restituisce solo le attività nuove e aggiorna il registro.
"""

import json
import argparse
import sys
from datetime import date
from pathlib import Path


def extract_place_id(maps_url: str) -> str | None:
    """Estrae il place_id dall'URL Google Maps di Apify."""
    if not maps_url:
        return None
    marker = "query_place_id="
    idx = maps_url.find(marker)
    if idx == -1:
        return None
    return maps_url[idx + len(marker):].split("&")[0]


def load_seen(seen_path: Path) -> dict:
    if seen_path.exists():
        with open(seen_path) as f:
            return json.load(f)
    return {"description": "Registro attività già estratte.", "last_updated": "", "places": []}


def save_seen(seen_path: Path, seen: dict) -> None:
    seen["last_updated"] = str(date.today())
    with open(seen_path, "w") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)


def deduplicate(raw_results: list[dict], seen: dict) -> tuple[list[dict], int]:
    """
    Ritorna (nuove_attività, n_duplicati).
    Ogni attività nuova viene aggiunta al registro seen in-place.
    """
    seen_ids = {p["place_id"] for p in seen["places"]}
    new_places = []
    duplicates = 0

    for item in raw_results:
        pid = extract_place_id(item.get("mapsUrl", ""))
        if not pid:
            # Nessun place_id → usa il nome come fallback
            pid = item.get("name", "").lower().replace(" ", "_")

        if pid in seen_ids:
            duplicates += 1
            continue

        new_places.append(item)
        seen_ids.add(pid)
        seen["places"].append({
            "place_id": pid,
            "name": item.get("name", ""),
            "address": item.get("address", ""),
            "added_on": str(date.today())
        })

    return new_places, duplicates


def main():
    parser = argparse.ArgumentParser(description="Deduplica attività Ticino da Apify.")
    parser.add_argument("--input", required=True, help="File JSON con i risultati grezzi di Apify")
    parser.add_argument("--seen", default="memory/seen_places.json", help="Registro seen_places.json")
    parser.add_argument("--output", default=".tmp/new_places.json", help="Output con sole attività nuove")
    parser.add_argument("--dry-run", action="store_true", help="Non aggiorna il registro seen")
    args = parser.parse_args()

    input_path = Path(args.input)
    seen_path = Path(args.seen)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERRORE: file input non trovato: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        raw = json.load(f)

    seen = load_seen(seen_path)
    new_places, n_dup = deduplicate(raw, seen)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(new_places, f, ensure_ascii=False, indent=2)

    if not args.dry_run:
        save_seen(seen_path, seen)

    print(f"Totale input:   {len(raw)}")
    print(f"Duplicati:      {n_dup}")
    print(f"Nuove attività: {len(new_places)}")
    print(f"Output:         {output_path}")
    if not args.dry_run:
        print(f"Registro seen aggiornato: {seen_path} ({len(seen['places'])} totali)")


if __name__ == "__main__":
    main()
