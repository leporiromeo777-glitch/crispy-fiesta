#!/usr/bin/env python3
"""
Webhook server — riceve POST da Zapier e lancia main.py
Avviare con: python3 execution/webhook.py
"""

import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 8080
MAIN = Path(__file__).parent / "main.py"


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/run":
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK — scout avviato\n")

        # Lancia main.py in background
        subprocess.Popen([sys.executable, str(MAIN)])

    def log_message(self, format, *args):
        print(f"[webhook] {self.address_string()} {format % args}")


if __name__ == "__main__":
    print(f"🌐 Webhook in ascolto su http://0.0.0.0:{PORT}/run")
    HTTPServer(("0.0.0.0", PORT), WebhookHandler).serve_forever()
