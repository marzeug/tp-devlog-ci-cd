# Image d'exécution : le jar est construit par la CI (étape package), pas dans Docker
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app
COPY target/calculator-api.jar app.jar

ENV PORT=8080
EXPOSE 8080

# Docker surveille lui-même l'état de l'application
HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:8080/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
