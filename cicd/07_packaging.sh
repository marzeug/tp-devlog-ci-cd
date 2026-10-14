#!/bin/bash
# Étape 7 : création du jar exécutable (target/employe.jar)




mvn package -DskipTests
if [ $? -ne 0 ]; then
    echo "ERREUR : le packaging a échoué"
    exit 1
fi

if [ ! -f target/employe.jar ]; then
    echo "ERREUR : le jar n'a pas été créé"
    exit 1
fi

echo "Packaging OK : target/employe.jar"
exit 0
