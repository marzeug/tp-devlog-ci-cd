"""Fonctions et configuration partagées par toutes les étapes de la CI/CD.

Convention : chaque étape est un script autonome qui renvoie
    0  -> succès
    1  -> échec
Le script global (pipeline.py) se base uniquement sur ce code retour.
"""
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# --- Configuration -----------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent  # racine du projet Java
APP_NAME = "calculator-api"
IMAGE = APP_NAME                     # nom de l'image Docker
CONTAINER = APP_NAME                 # nom du conteneur déployé
APP_PORT = int(os.environ.get("APP_PORT", "8080"))
BASE_URL = f"http://localhost:{APP_PORT}"
JAR = ROOT / "target" / f"{APP_NAME}.jar"
ARTIFACTS = ROOT / "artifacts"

SUCCESS = 0
FAILURE = 1

# Identifiants transmis par pipeline.py (valeurs par défaut si une étape est lancée seule)
BUILD_ID = os.environ.get("CI_BUILD_ID", time.strftime("%Y%m%d-%H%M%S"))
COMMIT = os.environ.get("CI_COMMIT", "local")


def log(message):
    print(message, flush=True)


def which(tool):
    """Chemin de l'exécutable (gère mvn.cmd / npx.cmd sous Windows)."""
    return shutil.which(tool)


def run(cmd, cwd=ROOT, capture=False):
    """Exécute une commande. Renvoie le code retour (et la sortie si capture=True)."""
    executable = which(cmd[0])
    if executable is None:
        log(f"[ERREUR] Commande introuvable : {cmd[0]}")
        return (127, "") if capture else 127
    full_cmd = [executable, *cmd[1:]]
    log(f"$ {' '.join(cmd)}")
    if capture:
        result = subprocess.run(full_cmd, cwd=cwd, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
        return result.returncode, (result.stdout + result.stderr).strip()
    return subprocess.run(full_cmd, cwd=cwd).returncode


def mvn(*goals):
    """Lance Maven en mode non interactif (batch)."""
    return run(["mvn", "-B", "--no-transfer-progress", *goals])


def docker(*args, capture=False):
    return run(["docker", *args], capture=capture)


def http_get(url, timeout=3):
    """Renvoie (code HTTP, corps) ou (None, message d'erreur)."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        return None, str(e)


def wait_healthy(timeout=40):
    """Attend que GET /health réponde {"status": "UP"}."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        status, body = http_get(f"{BASE_URL}/health")
        if status == 200:
            try:
                if json.loads(body).get("status") == "UP":
                    log(f"Application en bonne santé : {body}")
                    return True
            except json.JSONDecodeError:
                pass
        time.sleep(2)
    log(f"[ERREUR] L'application ne répond pas sur {BASE_URL}/health après {timeout}s")
    return False


def exit_with(ok):
    sys.exit(SUCCESS if ok else FAILURE)
