package fr.devlog.calculator;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class CalculatorTest {

    private final Calculator calculator = new Calculator();

    @Test
    void addition() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    void soustraction() {
        assertEquals(-1, calculator.subtract(2, 3));
    }

    @Test
    void multiplication() {
        assertEquals(6, calculator.multiply(2, 3));
    }

    @Test
    void division() {
        assertEquals(3, calculator.divide(7, 2));
    }

    @Test
    void divisionParZero() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(1, 0));
    }

    @Test
    void depassementDeCapacite() {
        assertThrows(ArithmeticException.class, () -> calculator.add(Integer.MAX_VALUE, 1));
    }

    @Test
    void computeParNom() {
        assertEquals(5, calculator.compute("add", 2, 3));
        assertEquals(-1, calculator.compute("subtract", 2, 3));
        assertEquals(6, calculator.compute("multiply", 2, 3));
        assertEquals(2, calculator.compute("divide", 4, 2));
    }

    @Test
    void operationInconnue() {
        assertThrows(IllegalArgumentException.class, () -> calculator.compute("modulo", 1, 2));
    }
}
