#!/bin/bash


mvn dependency:resolve
if [ $? -ne 0 ]; then
    echo "ERREUR : impossible de récupérer les dépendances"
    exit 1
fi

echo "Dépendances OK"
exit 0
