"""Rollback : redéploie la dernière version stable (image calculator-api:stable).

Appelé automatiquement par pipeline.py quand le déploiement ou les tests
d'intégration échouent. Peut aussi être lancé à la main.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import APP_PORT, CONTAINER, IMAGE, docker, exit_with, log, wait_healthy  # noqa: E402

STABLE = f"{IMAGE}:stable"

if __name__ == "__main__":
    # On retire dans tous les cas la version défaillante
    docker("rm", "-f", CONTAINER, capture=True)

    if docker("image", "inspect", STABLE, capture=True)[0] != 0:
        log("[ERREUR] Aucune version stable disponible : l'application défaillante a été arrêtée, "
            "aucun rollback possible")
        exit_with(False)

    if docker("run", "-d", "--name", CONTAINER, "-p", f"{APP_PORT}:8080", STABLE) != 0:
        exit_with(False)
    ok = wait_healthy()
    log("Rollback réussi : version stable restaurée" if ok else "[ERREUR] Échec du rollback")
    exit_with(ok)
