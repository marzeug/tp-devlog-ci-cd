package fr.devlog.calculator;

/**
 * Logique métier : opérations arithmétiques sur des entiers.
 */
public final class Calculator {

    public int add(int a, int b) {
        return Math.addExact(a, b);
    }

    public int subtract(int a, int b) {
        return Math.subtractExact(a, b);
    }

    public int multiply(int a, int b) {
        return Math.multiplyExact(a, b);
    }

    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division par zero impossible");
        }
        return a / b;
    }

    /**
     * Applique l'opération nommée (add, subtract, multiply, divide).
     *
     * @throws IllegalArgumentException si l'opération est inconnue
     */
    public int compute(String operation, int a, int b) {
        switch (operation) {
            case "add":
                return add(a, b);
            case "subtract":
                return subtract(a, b);
            case "multiply":
                return multiply(a, b);
            case "divide":
                return divide(a, b);
            default:
                throw new IllegalArgumentException("Operation inconnue : " + operation);
        }
    }
}
