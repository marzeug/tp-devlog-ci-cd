"""Étape R&D : contrôle de la qualité du code (Checkstyle, règles dans config/checkstyle.xml)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import exit_with, mvn  # noqa: E402

if __name__ == "__main__":
    exit_with(mvn("checkstyle:check") == 0)
