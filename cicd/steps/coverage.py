"""Étape R&D : mesure de la couverture des tests unitaires (JaCoCo).

Utilise le fichier target/jacoco.exec produit pendant l'étape des tests,
génère le rapport HTML (target/site/jacoco/index.html) et échoue si la
couverture de lignes est inférieure au seuil défini dans pom.xml.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import ROOT, exit_with, log, mvn  # noqa: E402

REPORT_CSV = ROOT / "target" / "site" / "jacoco" / "jacoco.csv"


def print_report():
    if not REPORT_CSV.exists():
        return
    covered_total = missed_total = 0
    with REPORT_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            missed, covered = int(row["LINE_MISSED"]), int(row["LINE_COVERED"])
            missed_total += missed
            covered_total += covered
            ratio = 100 * covered / (covered + missed) if covered + missed else 100
            log(f"  {row['CLASS']:<20} {ratio:6.1f} % des lignes")
    total = covered_total + missed_total
    log(f"  {'TOTAL':<20} {100 * covered_total / total if total else 100:6.1f} %")


if __name__ == "__main__":
    if not (ROOT / "target" / "jacoco.exec").exists():
        log("[ERREUR] target/jacoco.exec absent : l'étape des tests doit être exécutée avant")
        exit_with(False)
    report_ok = mvn("jacoco:report") == 0
    print_report()
    exit_with(report_ok and mvn("jacoco:check") == 0)
