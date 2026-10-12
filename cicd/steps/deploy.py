"""Étape 6 : déploiement dans un conteneur Docker.

1. construit l'image calculator-api:<build>
2. remplace le conteneur en cours d'exécution
3. vérifie que l'application répond sur /health
En cas d'échec, pipeline.py déclenche rollback.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import APP_PORT, BUILD_ID, CONTAINER, IMAGE, docker, exit_with, log, wait_healthy  # noqa: E402

if __name__ == "__main__":
    if docker("info", capture=True)[0] != 0:
        log("[ERREUR] Le démon Docker ne répond pas (Docker Desktop est-il démarré ?)")
        exit_with(False)

    tag = f"{IMAGE}:{BUILD_ID}"
    if docker("build", "-t", tag, "-t", f"{IMAGE}:latest", ".") != 0:
        exit_with(False)

    # Suppression de l'ancien conteneur (ignoré s'il n'existe pas)
    docker("rm", "-f", CONTAINER, capture=True)
    if docker("run", "-d", "--name", CONTAINER, "-p", f"{APP_PORT}:8080", tag) != 0:
        exit_with(False)

    healthy = wait_healthy()
    if not healthy:
        log("Derniers logs du conteneur :")
        log(docker("logs", "--tail", "30", CONTAINER, capture=True)[1])
    exit_with(healthy)
