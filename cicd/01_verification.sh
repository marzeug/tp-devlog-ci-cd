#!/bin/bash
# Étape 1 : vérification du projet et du manifest (pom.xml)

echo "Vérification des fichiers du projet..."

if [ ! -f pom.xml ]; then
    echo "ERREUR : pom.xml introuvable"
    exit 1
fi

if [ ! -f Dockerfile ]; then
    echo "ERREUR : Dockerfile introuvable"
    exit 1
fi

if [ ! -d src ]; then
    echo "ERREUR : dossier src introuvable"
    exit 1
fi

echo "Vérification du pom.xml..."
mvn validate
if [ $? -ne 0 ]; then
    echo "ERREUR : le pom.xml n'est pas valide"
    exit 1
fi

echo "Vérification OK"
exit 0
