#!/bin/bash
# Étape 6 : couverture de code avec JaCoCo
# JaCoCo a enregistré les lignes exécutées pendant les tests de l'étape 5.

echo "Génération du rapport de couverture..."
mvn jacoco:report
if [ $? -ne 0 ]; then
    echo "ERREUR : impossible de générer le rapport"
    exit 1
fi
echo "Rapport disponible dans app/target/site/jacoco/index.html"

echo "Vérification du seuil minimum de couverture (défini dans le pom.xml)..."
mvn jacoco:check
if [ $? -ne 0 ]; then
    echo "ERREUR : la couverture de code est trop faible"
    exit 1
fi

echo "Couverture OK"
exit 0
