"""Étape 1 : vérification de l'état du projet et du manifest (pom.xml)."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import ROOT, exit_with, log, run, which  # noqa: E402

REQUIRED_PATHS = ["pom.xml", "Dockerfile", "src/main/java", "src/test/java"]
REQUIRED_TOOLS = ["git", "java", "mvn", "docker"]
NS = {"m": "http://maven.apache.org/POM/4.0.0"}


def check_files():
    ok = True
    for rel in REQUIRED_PATHS:
        present = (ROOT / rel).exists()
        log(f"  {'OK ' if present else 'KO '} {rel}")
        ok &= present
    return ok


def check_manifest():
    try:
        pom = ET.parse(ROOT / "pom.xml").getroot()
    except ET.ParseError as e:
        log(f"[ERREUR] pom.xml invalide : {e}")
        return False
    fields = {name: pom.findtext(f"m:{name}", namespaces=NS) for name in ("groupId", "artifactId", "version")}
    log(f"  Manifest : {fields['groupId']}:{fields['artifactId']}:{fields['version']}")
    missing = [name for name, value in fields.items() if not value]
    if missing:
        log(f"[ERREUR] Champs manquants dans pom.xml : {missing}")
    return not missing


def check_tools():
    ok = True
    for tool in REQUIRED_TOOLS:
        path = which(tool)
        log(f"  {'OK ' if path else 'KO '} {tool} {path or '(introuvable)'}")
        ok &= path is not None
    return ok


def check_git():
    code, commit = run(["git", "rev-parse", "--short", "HEAD"], capture=True)
    if code != 0:
        log("[ERREUR] Le projet n'est pas un dépôt Git ou ne contient aucun commit")
        return False
    _, branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture=True)
    _, changes = run(["git", "status", "--porcelain"], capture=True)
    log(f"  Branche {branch}, commit {commit}")
    if changes:
        log("  [ATTENTION] Modifications non commitées présentes dans le dépôt")
    return True


if __name__ == "__main__":
    log("Fichiers obligatoires :")
    files_ok = check_files()
    log("Manifest Maven :")
    manifest_ok = files_ok and check_manifest()
    log("Outils nécessaires :")
    tools_ok = check_tools()
    log("Dépôt Git :")
    git_ok = check_git()
    exit_with(files_ok and manifest_ok and tools_ok and git_ok)
