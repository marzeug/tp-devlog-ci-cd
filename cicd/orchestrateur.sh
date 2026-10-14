#!/bin/bash


mkdir -p logs
cd app

for etape in 01_verification 02_lint 03_dependances 04_build 05_tests 06_couverture 07_packaging 08_deploiement
do
    echo "Etape : $etape"

    bash ../cicd/$etape.sh >> ../logs/pipeline.log 2>&1

    if [ $? -ne 0 ]; then
        echo "Echec de l'etape $etape"

        
        if [ "$etape" = "08_deploiement" ]; then
            echo "Etape : 09_rollback"
            bash ../cicd/09_rollback.sh >> ../logs/pipeline.log 2>&1
        fi

        exit 1
    fi
done

echo "Pipeline terminee avec succes"
