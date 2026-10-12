package fr.devlog.calculator;

import java.io.IOException;

/**
 * Point d'entrée de l'application.
 */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) throws IOException {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        String version = Main.class.getPackage().getImplementationVersion();
        ApiServer server = new ApiServer(port, version == null ? "dev" : version);
        server.start();
        System.out.println("Calculator API demarree sur le port " + port);
    }
}
