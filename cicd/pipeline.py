"""Script global de la CI/CD : exécute chaque étape dans l'ordre et journalise tout.

Usage :
    python cicd/pipeline.py              # pipeline complète
    python cicd/pipeline.py --no-deploy  # s'arrête après le packaging (sans Docker)

Logs :
    logs/pipeline_<build>.log  -> sortie détaillée de chaque étape
    logs/history.log           -> une ligne par exécution (date, commit, statut, durée)
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

CICD_DIR = Path(__file__).resolve().parent
ROOT = CICD_DIR.parent
STEPS_DIR = CICD_DIR / "steps"
LOGS_DIR = ROOT / "logs"

# (nom affiché, script, étape de déploiement ?)
STEPS = [
    ("Vérification du projet / manifest", "check_project.py", False),
    ("Gestion des dépendances", "dependencies.py", False),
    ("Compilation", "compile.py", False),
    ("Tests unitaires", "unit_tests.py", False),
    ("[R&D] Couverture de code (JaCoCo)", "coverage.py", False),
    ("[R&D] Qualité de code (Checkstyle)", "quality.py", False),
    ("Packaging", "package.py", False),
    ("Déploiement Docker", "deploy.py", True),
    ("[R&D] Tests d'intégration (Postman)", "integration_tests.py", True),
    ("Promotion en version stable", "promote.py", True),
]
STEP_TIMEOUT = 600  # secondes


class Logger:
    """Écrit simultanément sur la console et dans le fichier de log du build."""

    def __init__(self, path):
        self.file = path.open("w", encoding="utf-8")

    def __call__(self, message=""):
        line = f"[{time.strftime('%H:%M:%S')}] {message}"
        print(line, flush=True)
        self.file.write(line + "\n")
        self.file.flush()

    def close(self):
        self.file.close()


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip() or "inconnu"
    except FileNotFoundError:
        return "inconnu"


def run_step(log, name, script, env):
    """Lance un script d'étape, recopie sa sortie dans les logs, renvoie (code, durée)."""
    log(f"===== ÉTAPE : {name} =====")
    start = time.time()
    process = subprocess.Popen(
        [sys.executable, str(STEPS_DIR / script)], cwd=ROOT, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    try:
        for line in process.stdout:
            log(f"    {line.rstrip()}")
        code = process.wait(timeout=STEP_TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        log(f"    [ERREUR] Timeout de {STEP_TIMEOUT}s dépassé")
        code = 124
    duration = time.time() - start
    log(f"===== {name} : {'SUCCÈS' if code == 0 else f'ÉCHEC (code {code})'} en {duration:.1f}s =====")
    log()
    return code, duration


def main():
    parser = argparse.ArgumentParser(description="CI/CD from scratch")
    parser.add_argument("--no-deploy", action="store_true", help="ne pas exécuter les étapes Docker")
    args = parser.parse_args()

    build_id = time.strftime("%Y%m%d-%H%M%S")
    commit = git_commit()
    LOGS_DIR.mkdir(exist_ok=True)
    log = Logger(LOGS_DIR / f"pipeline_{build_id}.log")

    env = {**os.environ, "CI_BUILD_ID": build_id, "CI_COMMIT": commit, "PYTHONIOENCODING": "utf-8"}
    steps = [s for s in STEPS if not (args.no_deploy and s[2])]

    log(f"Pipeline {build_id} - commit {commit} - {len(steps)} étapes")
    log()
    start = time.time()
    results = []
    failed = None
    for name, script, is_deploy_step in steps:
        code, duration = run_step(log, name, script, env)
        results.append((name, code, duration))
        if code != 0:
            failed = (name, is_deploy_step)
            break

    if failed and failed[1]:
        log("Échec après le déploiement : lancement du rollback")
        code, duration = run_step(log, "Rollback", "rollback.py", env)
        results.append(("Rollback", code, duration))

    total = time.time() - start
    status = "SUCCÈS" if failed is None else f"ÉCHEC ({failed[0]})"
    log("===== RÉCAPITULATIF =====")
    for name, code, duration in results:
        log(f"  {'OK ' if code == 0 else 'KO '} {name:<40} {duration:6.1f}s")
    for name, _, _ in steps[len(results):]:
        log(f"  --  {name:<40} non exécutée")
    log(f"Résultat : {status} en {total:.1f}s")
    log.close()

    with (LOGS_DIR / "history.log").open("a", encoding="utf-8") as history:
        history.write(f"{build_id} commit={commit} statut={status} durée={total:.1f}s\n")

    return 0 if failed is None else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
