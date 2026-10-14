#!/bin/bash

mvn checkstyle:check
if [ $? -ne 0 ]; then
    echo "ERREUR : le code ne respecte pas les règles de qualité"
    exit 1
fi

echo "Lint OK"
exit 0
