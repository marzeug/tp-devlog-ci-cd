# TP DEVLOG : CI/CD « from scratch »

Le microservice **Employé** (Spring Boot + base H2) et une CI/CD écrite en scripts shell.

## Arborescence

```
sujet tp devlog/
├── app/                          le microservice Employé
│   ├── pom.xml                   manifest Maven
│   ├── checkstyle.xml            règles du lint
│   ├── Dockerfile                image Docker de l'application
│   └── src/
│       ├── main/java/projet/microservices/employe/
│       │   ├── EmployeApplication.java      point d'entrée Spring Boot
│       │   ├── JerseyConfig.java            expose l'API sous /api
│       │   ├── application/                 Employe, EmployeService
│       │   ├── infrastructure/              EmployeRepository (base H2)
│       │   └── presentation/                webservices REST + DTO
│       └── test/java/projet/microservices/employe/
├── cicd/                         la CI/CD
│   ├── orchestrateur.sh          lance toutes les étapes depuis app/ + logs
│   ├── 01_verification.sh        mvn validate
│   ├── 02_lint.sh                Checkstyle : qualité du code
│   ├── 03_dependances.sh         mvn dependency:resolve
│   ├── 04_build.sh               mvn clean compile
│   ├── 05_tests.sh               mvn test
│   ├── 06_couverture.sh          JaCoCo : couverture de code
│   ├── 07_packaging.sh           mvn package
│   ├── 08_deploiement.sh         docker build + docker run
│   └── 09_rollback.sh            remet la dernière version stable
└── logs/                         logs de toutes les exécutions (pipeline.log)
```

## Lancer la pipeline

Dans Git Bash, avec Docker Desktop démarré :

```bash
bash cicd/orchestrateur.sh
```

Puis tester l'application :

```bash
# Créer un employé
curl -X POST http://localhost:8081/api/employes -H "Content-Type: application/json" -d '{"nom":"Dupont"}'

# Lister les employés
curl http://localhost:8081/api/employes
```

## Fonctionnement

- Chaque script renvoie `0` si l'étape réussit, `1` si elle échoue.
- `orchestrateur.sh` se place dans `app/` puis lance les étapes 1 à 8 dans l'ordre et s'arrête à la première erreur.
- Tout ce qu'affichent les étapes est écrit dans `logs/pipeline.log`.
- Si le déploiement réussit, l'image Docker est sauvegardée sous le nom `employe:stable`.
- Si le déploiement échoue, l'orchestrateur lance `09_rollback.sh`, qui redémarre cette version stable.
