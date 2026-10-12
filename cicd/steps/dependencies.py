"""Étape 2 : gestion des dépendances (téléchargement dans le dépôt local Maven)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import exit_with, mvn  # noqa: E402

if __name__ == "__main__":
    exit_with(mvn("dependency:resolve", "dependency:resolve-plugins") == 0)
