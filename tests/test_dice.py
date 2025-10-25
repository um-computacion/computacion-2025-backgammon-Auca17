import unittest
from unittest.mock import patch
from core.dice import Dice

# Sino pongo ,from unittest.mock import patch, no me deja ejecutar los @patch


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_init(self):
        """Verifica que los valores de los dados son None inicialmente."""
        self.assertIsNone(self.dice.__value1__)
        self.assertIsNone(self.dice.__value2__)

    @patch("core.dice.random.randint")
    def test_roll(self, mock_randint):
        """Verifica que roll establece los valores usando random.randint."""
        mock_randint.side_effect = [3, 5]
        self.dice.roll()
        self.assertEqual(self.dice.__value1__, 3)
        self.assertEqual(self.dice.__value2__, 5)
        self.assertEqual(mock_randint.call_count, 2)

    def test_get_values(self):
        """Verifica que get_values devuelve una tupla de los valores actuales."""
        self.dice.__value1__ = 2
        self.dice.__value2__ = 4
        self.assertEqual(self.dice.get_values(), (2, 4))

    def test_is_double_true(self):
        """Verifica que is_double devuelve True cuando los valores son iguales."""
        self.dice.__value1__ = 3
        self.dice.__value2__ = 3
        self.assertTrue(self.dice.is_double())

    def test_is_double_false(self):
        """Verifica que is_double devuelve False cuando los valores no son iguales."""
        self.dice.__value1__ = 2
        self.dice.__value2__ = 6
        self.assertFalse(self.dice.is_double())


if __name__ == "__main__":
    unittest.main()
