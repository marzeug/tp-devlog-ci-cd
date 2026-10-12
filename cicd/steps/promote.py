"""Étape finale : la version déployée a passé tous les contrôles, elle devient la version stable.

L'image taguée calculator-api:stable est celle que rollback.py redéploiera
si un déploiement futur échoue.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import BUILD_ID, IMAGE, exit_with, log, docker  # noqa: E402

if __name__ == "__main__":
    ok = docker("tag", f"{IMAGE}:{BUILD_ID}", f"{IMAGE}:stable") == 0
    if ok:
        log(f"{IMAGE}:{BUILD_ID} est maintenant la version stable")
    exit_with(ok)
