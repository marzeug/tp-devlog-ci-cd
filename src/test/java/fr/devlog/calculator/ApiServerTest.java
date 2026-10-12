package fr.devlog.calculator;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ApiServerTest {

    private ApiServer server;
    private final HttpClient client = HttpClient.newHttpClient();

    @BeforeEach
    void start() throws Exception {
        server = new ApiServer(0, "test");
        server.start();
    }

    @AfterEach
    void stop() {
        server.stop();
    }

    private HttpResponse<String> call(String method, String path) throws Exception {
        HttpRequest request = HttpRequest.newBuilder(URI.create("http://localhost:" + server.getPort() + path))
                .method(method, HttpRequest.BodyPublishers.noBody())
                .build();
        return client.send(request, HttpResponse.BodyHandlers.ofString());
    }

    @Test
    void health() throws Exception {
        HttpResponse<String> response = call("GET", "/health");
        assertEquals(200, response.statusCode());
        assertEquals("{\"status\":\"UP\",\"version\":\"test\"}", response.body());
    }

    @Test
    void addition() throws Exception {
        HttpResponse<String> response = call("GET", "/api/add?a=2&b=3");
        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("\"result\":5"));
    }

    @Test
    void parametresInvalides() throws Exception {
        assertEquals(400, call("GET", "/api/add?a=x&b=3").statusCode());
        assertEquals(400, call("GET", "/api/add").statusCode());
    }

    @Test
    void divisionParZero() throws Exception {
        assertEquals(400, call("GET", "/api/divide?a=1&b=0").statusCode());
    }

    @Test
    void operationInconnue() throws Exception {
        assertEquals(404, call("GET", "/api/modulo?a=1&b=2").statusCode());
    }

    @Test
    void methodeNonAutorisee() throws Exception {
        assertEquals(405, call("POST", "/api/add?a=1&b=2").statusCode());
    }

    @Test
    void parseQuery() {
        assertEquals(Map.of("a", "1", "b", ""), ApiServer.parseQuery("a=1&b"));
        assertTrue(ApiServer.parseQuery(null).isEmpty());
        assertTrue(ApiServer.parseQuery("").isEmpty());
    }
}
