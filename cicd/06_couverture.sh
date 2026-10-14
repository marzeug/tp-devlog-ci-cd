#!/bin/bash


mvn jacoco:report
if [ $? -ne 0 ]; then
    echo "ERREUR : impossible de générer le rapport"
    exit 1
fi
echo "Rapport disponible dans app/target/site/jacoco/index.html"


mvn jacoco:check
if [ $? -ne 0 ]; then
    echo "ERREUR : la couverture de code est trop faible"
    exit 1
fi

echo "Couverture OK"
exit 0
