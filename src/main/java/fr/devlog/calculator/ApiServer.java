package fr.devlog.calculator;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Serveur HTTP minimaliste (JDK uniquement) exposant la calculatrice.
 *
 * <ul>
 *   <li>GET /health : état de l'application (utilisé par le déploiement)</li>
 *   <li>GET /api/{operation}?a=..&amp;b=.. : calcul</li>
 * </ul>
 */
public final class ApiServer {

    private static final String API_PREFIX = "/api/";

    private final HttpServer server;
    private final Calculator calculator = new Calculator();
    private final String version;

    public ApiServer(int port, String version) throws IOException {
        this.version = version;
        this.server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/health", this::handleHealth);
        server.createContext(API_PREFIX, this::handleApi);
    }

    public void start() {
        server.start();
    }

    public void stop() {
        server.stop(0);
    }

    public int getPort() {
        return server.getAddress().getPort();
    }

    private void handleHealth(HttpExchange exchange) throws IOException {
        send(exchange, 200, "{\"status\":\"UP\",\"version\":\"" + version + "\"}");
    }

    private void handleApi(HttpExchange exchange) throws IOException {
        if (!"GET".equals(exchange.getRequestMethod())) {
            send(exchange, 405, error("Methode non autorisee"));
            return;
        }
        String operation = exchange.getRequestURI().getPath().substring(API_PREFIX.length());
        Map<String, String> params = parseQuery(exchange.getRequestURI().getRawQuery());
        try {
            int a = Integer.parseInt(params.get("a"));
            int b = Integer.parseInt(params.get("b"));
            int result = calculator.compute(operation, a, b);
            send(exchange, 200, String.format(
                    "{\"operation\":\"%s\",\"a\":%d,\"b\":%d,\"result\":%d}", operation, a, b, result));
        } catch (NumberFormatException e) {
            send(exchange, 400, error("Parametres a et b entiers obligatoires"));
        } catch (IllegalArgumentException e) {
            send(exchange, 404, error(e.getMessage()));
        } catch (ArithmeticException e) {
            send(exchange, 400, error(e.getMessage()));
        }
    }

    static Map<String, String> parseQuery(String query) {
        Map<String, String> params = new HashMap<>();
        if (query == null || query.isEmpty()) {
            return params;
        }
        for (String pair : query.split("&")) {
            String[] kv = pair.split("=", 2);
            params.put(kv[0], kv.length > 1 ? kv[1] : "");
        }
        return params;
    }

    private static String error(String message) {
        return "{\"error\":\"" + message + "\"}";
    }

    private static void send(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
