# Automated Reports

## Coverage Report

```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
core/__init__.py       0      0   100%
core/board.py         98      3    97%   106-107, 171
core/checker.py       14      0   100%
core/dice.py          12      0   100%
core/game.py         159      6    96%   144-145, 165, 188, 233, 292
core/player.py        31      1    97%   39
------------------------------------------------
TOTAL                314     10    97%

```

## Pylint Report

```text
************* Module cli.cli
cli/cli.py:94:0: C0301: Line too long (116/100) (line-too-long)
cli/cli.py:39:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
************* Module core.checker
core/checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.game
core/game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/game.py:76:8: C2801: Unnecessarily calls dunder method __init__. Instantiate class directly. (unnecessary-dunder-call)
core/game.py:105:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/game.py:139:20: W0612: Unused variable '__die__' (unused-variable)
core/game.py:274:22: R1714: Consider merging these comparisons with 'in' by using '__to_pos__ in (24, -1)'. Use a set instead if elements are hashable. (consider-using-in)
core/game.py:1:0: W0611: Unused Board imported from core.board (unused-import)
core/game.py:2:0: W0611: Unused Player imported from core.player (unused-import)
core/game.py:3:0: W0611: Unused Dice imported from core.dice (unused-import)
************* Module core.board
core/board.py:11:0: C0301: Line too long (107/100) (line-too-long)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:13:23: W0622: Redefining built-in '__name__' (redefined-builtin)
************* Module core.dice
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_checker
tests/test_checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_checker.py:5:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_game
tests/test_game.py:227:0: C0301: Line too long (105/100) (line-too-long)
tests/test_game.py:136:12: W0612: Unused variable 'i' (unused-variable)
tests/test_game.py:198:24: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
tests/test_game.py:208:25: W0212: Access to a protected member _can_bear_off of a client class (protected-access)
tests/test_game.py:249:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:270:12: W0212: Access to a protected member _validate_move of a client class (protected-access)
tests/test_game.py:330:12: W0212: Access to a protected member _validate_bear_off of a client class (protected-access)
tests/test_game.py:347:12: W0212: Access to a protected member _validate_reentry of a client class (protected-access)
tests/test_game.py:357:12: W0212: Access to a protected member _validate_move of a client class (protected-access)
tests/test_game.py:379:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:405:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:415:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:149:8: W0201: Attribute '__player__' defined outside __init__ (attribute-defined-outside-init)
tests/test_game.py:13:0: R0904: Too many public methods (30/20) (too-many-public-methods)
************* Module tests.test_dice
tests/test_dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_dice.py:8:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_board
tests/test_board.py:9:0: C0115: Missing class docstring (missing-class-docstring)
tests/test_board.py:1:0: R0801: Similar lines in 2 files
==tests.test_exceptions:[20:30]
==tests.test_game:[21:36]
        self.__player1__ = Player("Alice", "white")
        self.__player2__ = Player("Bob", "black")
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__game__ = Game(
            player1=self.__player1__,
            player2=self.__player2__,
            board=self.__board__,
            dice=self.__dice__,
        )

    def test_initialization(self):
        """
        Verifica que el juego se inicializa correctamente.
        """ (duplicate-code)

-----------------------------------
Your code has been rated at 9.56/10


```
