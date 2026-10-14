#!/bin/bash

mvn clean compile
if [ $? -ne 0 ]; then
    echo "ERREUR : la compilation a échoué"
    exit 1
fi

echo "Compilation OK"
exit 0
