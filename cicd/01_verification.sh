#!/bin/bash



mvn validate
if [ $? -ne 0 ]; then
    echo "ERREUR : le pom.xml n'est pas valide"
    exit 1
fi

echo "Vérification OK"
exit 0
