"""Étape R&D : tests d'intégration sur l'application déployée (collection Postman exécutée par Newman)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import BASE_URL, ROOT, exit_with, run  # noqa: E402

COLLECTION = ROOT / "postman" / "calculator-api.postman_collection.json"
REPORT = ROOT / "target" / "newman-report.xml"

if __name__ == "__main__":
    code = run([
        "npx", "--yes", "newman@6", "run", str(COLLECTION),
        "--env-var", f"baseUrl={BASE_URL}",
        "--reporters", "cli,junit",
        "--reporter-junit-export", str(REPORT),
        "--color", "off",
    ])
    exit_with(code == 0)
