"""R&D : serveur WebHook GitHub qui déclenche la pipeline à chaque push.

    set WEBHOOK_SECRET=monSecret          (même secret que dans GitHub)
    python cicd/webhook_server.py         (écoute sur le port 9000)

GitHub doit pouvoir joindre la machine : en local, exposer le port avec
`ngrok http 9000` et déclarer https://<id>.ngrok-free.app/webhook dans
Settings > Webhooks du dépôt (content type : application/json).
"""
import hashlib
import hmac
import json
import os
import queue
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("WEBHOOK_PORT", "9000"))
SECRET = os.environ.get("WEBHOOK_SECRET", "").encode()
BRANCH = os.environ.get("WEBHOOK_BRANCH", "main")

# File d'attente : les pipelines s'exécutent une par une, jamais en parallèle
jobs = queue.Queue()


def signature_valid(body, header):
    if not SECRET:
        return True  # pas de secret configuré (déconseillé)
    expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header or "")


def worker():
    while True:
        commit = jobs.get()
        print(f"[webhook] Mise à jour du dépôt puis pipeline pour le commit {commit}", flush=True)
        if subprocess.run(["git", "pull", "--ff-only"], cwd=ROOT).returncode != 0:
            print("[webhook] git pull a échoué, pipeline non lancée", flush=True)
        else:
            code = subprocess.run([sys.executable, str(ROOT / "cicd" / "pipeline.py")], cwd=ROOT).returncode
            print(f"[webhook] Pipeline terminée avec le code {code}", flush=True)
        jobs.task_done()


class WebhookHandler(BaseHTTPRequestHandler):

    def reply(self, status, message):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode())

    def do_POST(self):
        if self.path != "/webhook":
            return self.reply(404, "not found")
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if not signature_valid(body, self.headers.get("X-Hub-Signature-256")):
            return self.reply(401, "signature invalide")

        event = self.headers.get("X-GitHub-Event")
        if event == "ping":
            return self.reply(200, "pong")
        if event != "push":
            return self.reply(200, f"événement {event} ignoré")

        payload = json.loads(body)
        if payload.get("ref") != f"refs/heads/{BRANCH}":
            return self.reply(200, f"branche {payload.get('ref')} ignorée")

        jobs.put(payload.get("after", "?")[:7])
        # GitHub attend une réponse rapide (< 10 s) : la pipeline tourne en arrière-plan
        self.reply(202, "pipeline planifiée")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    threading.Thread(target=worker, daemon=True).start()
    if not SECRET:
        print("[webhook] ATTENTION : WEBHOOK_SECRET non défini, les signatures ne sont pas vérifiées")
    print(f"[webhook] En écoute sur http://0.0.0.0:{PORT}/webhook (branche {BRANCH})", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), WebhookHandler).serve_forever()
