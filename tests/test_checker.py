import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):
    def test_initialization_valid_color(self):
        """
        Verifica que una ficha se inicializa correctamente con un color válido.
        Precondición: Se instancia un Checker con 'white'.
        Resultado esperado: El color es 'white' y no está capturada.
        """
        checker = Checker("white")
        self.assertEqual(checker.__color__, "white")
        self.assertFalse(checker.__is_captured__)
        self.assertIsNone(checker.__position__)

    def test_initialization_invalid_color(self):
        """
        Verifica que se lanza un ValueError si se usa un color inválido.
        Precondición: Se intenta instanciar un Checker con 'blue'.
        Resultado esperado: Se lanza un ValueError.
        """
        with self.assertRaises(ValueError):
            Checker("blue")

    def test_move_to(self):
        """
        Verifica que la posición de la ficha se actualiza correctamente.
        Precondición: Una ficha está en la posición inicial (None).
        Resultado esperado: La posición se actualiza a 5.
        """
        checker = Checker("black")
        checker.move_to(5)
        self.assertEqual(checker.__position__, 5)

    def test_capture(self):
        """
        Verifica que el estado de la ficha cambia a capturado.
        Precondición: Una ficha no está capturada.
        Resultado esperado: La ficha está marcada como capturada y su posición es 'bar'.
        """
        checker = Checker("white")
        checker.capture()
        self.assertTrue(checker.__is_captured__)
        self.assertEqual(checker.__position__, "bar")

    def test_repr(self):
        """
        Verifica que la representación en texto de la ficha es correcta.
        Precondición: Se crea una ficha de color 'black'.
        Resultado esperado: El __repr__ devuelve 'Checker(black)'.
        """
        checker = Checker("black")
        self.assertEqual(repr(checker), "Checker(black)")


if __name__ == "__main__":
    unittest.main()
