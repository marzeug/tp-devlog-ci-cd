#!/bin/bash

mvn test
if [ $? -ne 0 ]; then
    echo "ERREUR : des tests ont échoué"
    exit 1
fi

echo "Tests OK"
exit 0
