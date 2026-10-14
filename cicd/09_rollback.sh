#!/bin/bash



docker rm -f employe


docker run -d --name employe -p 8081:8081 employe:stable
if [ $? -ne 0 ]; then
    echo "ERREUR : aucune version stable disponible, rollback impossible"
    exit 1
fi

echo "Rollback OK "
exit 0
