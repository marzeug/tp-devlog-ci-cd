"""Étape 4 : exécution des tests unitaires (JUnit 5 via Surefire)."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import ROOT, exit_with, log, mvn  # noqa: E402


def summary():
    """Agrège les rapports Surefire pour afficher un bilan lisible dans les logs."""
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for report in (ROOT / "target" / "surefire-reports").glob("TEST-*.xml"):
        suite = ET.parse(report).getroot()
        for key in totals:
            totals[key] += int(suite.get(key, 0))
    log(f"Bilan : {totals['tests']} tests, {totals['failures']} échecs, "
        f"{totals['errors']} erreurs, {totals['skipped']} ignorés")


if __name__ == "__main__":
    code = mvn("test")
    summary()
    exit_with(code == 0)
