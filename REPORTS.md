# Automated Reports

## Coverage Report
```text
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
core/__init__.py               0      0   100%
core/board.py                 56     23    59%   30, 33, 35, 37, 41-42, 50-53, 61-70, 76, 82, 88, 96
core/checker.py               14      5    64%   17, 29, 35-36, 40
core/dice.py                  12      0   100%
core/game.py                  47     13    72%   34, 47-50, 56, 62, 68, 71, 74, 91-96
core/player.py                29      8    72%   22, 35-36, 43-44, 51, 58, 65
tests/test_board.py           14      1    93%   24
tests/test_dice.py            30      1    97%   42
tests/test_exceptions.py      16      1    94%   25
tests/test_game.py            22      1    95%   43
tests/test_player.py          20      1    95%   43
--------------------------------------------------------
TOTAL                        260     54    79%

```

## Pylint Report
```text
************* Module cli.cli
cli/cli.py:11:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:15:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:20:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:25:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:35:0: C0303: Trailing whitespace (trailing-whitespace)
cli/cli.py:41:0: C0304: Final newline missing (missing-final-newline)
cli/cli.py:1:0: C0114: Missing module docstring (missing-module-docstring)
cli/cli.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
cli/cli.py:8:14: E1120: No value for argument '__color__' in constructor call (no-value-for-parameter)
cli/cli.py:9:14: E1120: No value for argument '__color__' in constructor call (no-value-for-parameter)
************* Module core.checker
core/checker.py:40:0: C0304: Final newline missing (missing-final-newline)
core/checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.game
core/game.py:85:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/game.py:96:0: C0304: Final newline missing (missing-final-newline)
core/game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/game.py:34:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:50:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:42:19: W0613: Unused argument 'from_pos' (unused-argument)
core/game.py:42:29: W0613: Unused argument 'to_pos' (unused-argument)
core/game.py:56:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:62:8: W0107: Unnecessary pass statement (unnecessary-pass)
core/game.py:64:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:67:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:70:4: C0116: Missing function or method docstring (missing-function-docstring)
core/game.py:73:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.board
core/board.py:36:0: C0301: Line too long (145/100) (line-too-long)
core/board.py:40:0: C0301: Line too long (146/100) (line-too-long)
core/board.py:63:0: C0301: Line too long (125/100) (line-too-long)
core/board.py:67:0: C0301: Line too long (126/100) (line-too-long)
core/board.py:104:0: C0304: Final newline missing (missing-final-newline)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:3:0: C0115: Missing class docstring (missing-class-docstring)
************* Module core.exceptions
core/exceptions.py:7:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:11:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:15:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:19:4: W0107: Unnecessary pass statement (unnecessary-pass)
core/exceptions.py:23:4: W0107: Unnecessary pass statement (unnecessary-pass)
************* Module core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:6:23: W0622: Redefining built-in '__name__' (redefined-builtin)
core/player.py:36:16: E1101: Instance of 'Player' has no '__bar_checkers__' member (no-member)
core/player.py:43:11: E1101: Instance of 'Player' has no '__bar_checkers__' member (no-member)
core/player.py:44:12: E1101: Instance of 'Player' has no '__bar_checkers__' member (no-member)
core/player.py:51:8: E1101: Instance of 'Player' has no '__home_checkers__' member (no-member)
core/player.py:58:15: E1101: Instance of 'Player' has no '__bar_checkers__' member (no-member)
core/player.py:65:15: E1101: Instance of 'Player' has no '__home_checkers__' member (no-member)
************* Module core.dice
core/dice.py:28:0: C0304: Final newline missing (missing-final-newline)
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/dice.py:3:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_player
tests/test_player.py:19:0: C0301: Line too long (102/100) (line-too-long)
tests/test_player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_exceptions
tests/test_exceptions.py:25:0: C0304: Final newline missing (missing-final-newline)
tests/test_exceptions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_exceptions.py:5:0: C0115: Missing class docstring (missing-class-docstring)
tests/test_exceptions.py:9:4: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_exceptions.py:14:4: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_exceptions.py:19:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module tests.test_game
tests/test_game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_dice
tests/test_dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_dice.py:5:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_board
tests/test_board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_board.py:4:0: C0115: Missing class docstring (missing-class-docstring)
tests/test_board.py:8:4: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 6.82/10


```
