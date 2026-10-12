"""Étape 5 : packaging de l'application en jar exécutable + archivage de l'artefact."""
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import APP_NAME, ARTIFACTS, BUILD_ID, JAR, exit_with, log, mvn  # noqa: E402


def jar_is_executable():
    if not JAR.exists():
        log(f"[ERREUR] Jar introuvable : {JAR}")
        return False
    with zipfile.ZipFile(JAR) as jar:
        manifest = jar.read("META-INF/MANIFEST.MF").decode("utf-8")
    if "Main-Class:" not in manifest:
        log("[ERREUR] Le jar ne déclare pas de Main-Class")
        return False
    log(f"Jar valide : {JAR.name} ({JAR.stat().st_size} octets)")
    return True


if __name__ == "__main__":
    # Les tests ont déjà été exécutés par une étape dédiée
    if mvn("package", "-DskipTests") != 0 or not jar_is_executable():
        exit_with(False)
    ARTIFACTS.mkdir(exist_ok=True)
    archived = ARTIFACTS / f"{APP_NAME}-{BUILD_ID}.jar"
    shutil.copy2(JAR, archived)
    log(f"Artefact archivé : {archived}")
    exit_with(True)
