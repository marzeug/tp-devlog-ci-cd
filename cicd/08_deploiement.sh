#!/bin/bash

docker build -t employe:nouvelle .
if [ $? -ne 0 ]; then
    echo "ERREUR : la construction de l'image a échoué"
    exit 1
fi

docker rm -f employe

docker run -d --name employe -p 8081:8081 employe:nouvelle
if [ $? -ne 0 ]; then
    echo "ERREUR : le conteneur n'a pas démarré"
    exit 1
fi

docker tag employe:nouvelle employe:stable

echo "Déploiement OK "
exit 0
