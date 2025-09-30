import unittest
from unittest.mock import patch
from core.dice import Dice


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_init(self):
        """Test that dice values are None initially."""
        self.assertIsNone(self.dice.__value1__)
        self.assertIsNone(self.dice.__value2__)

    @patch("core.dice.random.randint")
    def test_roll(self, mock_randint):
        """Test that roll sets values using random.randint."""
        mock_randint.side_effect = [3, 5]
        self.dice.roll()
        self.assertEqual(self.dice.__value1__, 3)
        self.assertEqual(self.dice.__value2__, 5)
        self.assertEqual(mock_randint.call_count, 2)

    def test_get_values(self):
        """Test that get_values returns a tuple of current values."""
        self.dice.__value1__ = 2
        self.dice.__value2__ = 4
        self.assertEqual(self.dice.get_values(), (2, 4))

    def test_is_double_true(self):
        """Test is_double returns True when values are equal."""
        self.dice.__value1__ = 3
        self.dice.__value2__ = 3
        self.assertTrue(self.dice.is_double())

    def test_is_double_false(self):
        """Test is_double returns False when values are not equal."""
        self.dice.__value1__ = 2
        self.dice.__value2__ = 6
        self.assertFalse(self.dice.is_double())


if __name__ == "__main__":
    unittest.main()
