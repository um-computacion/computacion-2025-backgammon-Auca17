# Automated Reports

## Coverage Report
```text
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
core/__init__.py               0      0   100%
core/board.py                 56     23    59%   36, 39, 41, 47, 55-56, 64-70, 78-95, 101, 107, 113, 121
core/checker.py               14      5    64%   17, 29, 35-36, 40
core/dice.py                  12      0   100%
core/game.py                  47     13    72%   35, 48-51, 57, 63, 69, 72, 75, 92-97
core/player.py                31      8    74%   24, 37-38, 45-46, 53, 60, 67
tests/test_board.py           14      1    93%   30
tests/test_dice.py            30      1    97%   44
tests/test_exceptions.py      16      1    94%   27
tests/test_game.py            22      1    95%   44
tests/test_player.py          20      1    95%   45
--------------------------------------------------------
TOTAL                        262     54    79%

```

## Pylint Report
```text
************* Module cli.cli
cli/cli.py:1:0: C0114: Missing module docstring (missing-module-docstring)
cli/cli.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.checker
core/checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.game
core/game.py:86:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/game.py:35:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:51:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:43:19: W0613: Unused argument 'from_pos' (unused-argument)
core/game.py:43:29: W0613: Unused argument 'to_pos' (unused-argument)
core/game.py:57:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:63:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:65:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:68:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:71:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:74:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.board
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:4:0: C0115: Missing class docstring (missing-class-docstring)
************* Module core.exceptions
core/exceptions.py:9:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:15:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:21:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:27:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:33:4: W0107: Unnecessary pass statement (unnecessary-pass)
************* Module core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:6:23: W0622: Redefining built-in '__name__' (redefined-builtin)
************* Module core.dice
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/dice.py:4:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_player
tests/test_player.py:20:0: C0301: Line too long (102/100) (line-too-long)
tests/test_player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_exceptions
tests/test_exceptions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_exceptions.py:6:0: C0115: Missing class docstring (missing-class-docstring)
tests/test_exceptions.py:10:4: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_exceptions.py:15:4: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_exceptions.py:20:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module tests.test_game
tests/test_game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_dice
tests/test_dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_dice.py:6:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_board
tests/test_board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_board.py:5:0: C0115: Missing class docstring (missing-class-docstring)
tests/test_board.py:9:4: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 8.69/10


```
