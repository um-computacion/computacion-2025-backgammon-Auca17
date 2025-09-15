from core.board import Board
from core.checker import Checker

def test_board_has_points():
    b = Board()
    assert hasattr(b, "_Board__points__")

def test_checker_moves_and_capture():
    c = Checker("WHITE", 0)
    c.move_to(5)
    assert getattr(c, "_Checker__position__") == 5
    c.capture()
    assert getattr(c, "_Checker__is_captured__") is True
