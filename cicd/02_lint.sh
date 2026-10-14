#!/bin/bash
# Étape 2 : lint, contrôle de la qualité du code avec Checkstyle
# Les règles vérifiées sont dans app/checkstyle.xml

echo "Analyse du code..."
mvn checkstyle:check
if [ $? -ne 0 ]; then
    echo "ERREUR : le code ne respecte pas les règles de qualité"
    exit 1
fi

echo "Lint OK"
exit 0
