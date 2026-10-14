# Image avec Java pour exécuter l'application
FROM eclipse-temurin:21-jre

WORKDIR /app

# On copie le jar construit à l'étape de packaging
COPY target/employe.jar employe.jar

# Port du microservice (défini dans application.properties)
EXPOSE 8081

# Commande lancée au démarrage du conteneur
CMD ["java", "-jar", "employe.jar"]
