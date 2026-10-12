"""Étape 3 : compilation du projet (sources + tests)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import exit_with, mvn  # noqa: E402

if __name__ == "__main__":
    # clean : on repart toujours d'un état propre pour garantir la reproductibilité
    exit_with(mvn("clean", "test-compile") == 0)
