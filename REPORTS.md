# Automated Reports

## Coverage Report
```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cli/__init__.py          0      0   100%
cli/cli.py             114      6    95%   135, 157-159, 168, 180, 190
core/__init__.py         0      0   100%
core/board.py           98      0   100%
core/checker.py         12      0   100%
core/dice.py            12      0   100%
core/exceptions.py       5      0   100%
core/game.py           309     32    90%   281, 372-377, 451-453, 469, 478-481, 508-521, 536, 560, 564, 587, 600-605, 628
core/player.py          31      0   100%
--------------------------------------------------
TOTAL                  581     38    93%

```

## Pylint Report
```text
************* Module pygame_ui.main
pygame_ui/main.py:1:0: C0302: Too many lines in module (1283/1000) (too-many-lines)
pygame_ui/main.py:51:0: E1101: Module 'pygame' has no 'init' member (no-member)
pygame_ui/main.py:156:4: C0104: Disallowed name "bar" (disallowed-name)
pygame_ui/main.py:218:8: W0621: Redefining name 'i' from outer scope (line 109) (redefined-outer-name)
pygame_ui/main.py:260:4: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame_ui/main.py:260:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:260:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:260:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:229:0: R0912: Too many branches (31/12) (too-many-branches)
pygame_ui/main.py:229:0: R0915: Too many statements (53/50) (too-many-statements)
pygame_ui/main.py:260:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:397:8: W0621: Redefining name 'i' from outer scope (line 109) (redefined-outer-name)
pygame_ui/main.py:443:0: R0914: Too many local variables (27/15) (too-many-locals)
pygame_ui/main.py:466:8: W0621: Redefining name 'i' from outer scope (line 109) (redefined-outer-name)
pygame_ui/main.py:456:4: W0612: Unused variable 'shadow_color' (unused-variable)
pygame_ui/main.py:512:0: R0914: Too many local variables (28/15) (too-many-locals)
pygame_ui/main.py:526:12: W0621: Redefining name 'i' from outer scope (line 109) (redefined-outer-name)
pygame_ui/main.py:517:4: C0104: Disallowed name "bar" (disallowed-name)
pygame_ui/main.py:652:0: R0914: Too many local variables (16/15) (too-many-locals)
pygame_ui/main.py:784:0: R0914: Too many local variables (17/15) (too-many-locals)
pygame_ui/main.py:834:0: R0914: Too many local variables (21/15) (too-many-locals)
pygame_ui/main.py:953:4: C0103: Variable name "A" doesn't conform to snake_case naming style (invalid-name)
pygame_ui/main.py:994:8: W0621: Redefining name 'i' from outer scope (line 109) (redefined-outer-name)
pygame_ui/main.py:980:7: W0612: Unused variable 'y' (unused-variable)
pygame_ui/main.py:1001:30: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1003:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1012:36: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1014:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1041:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1045:24: E1101: Module 'pygame' has no 'K_BACKSPACE' member (no-member)
pygame_ui/main.py:1054:36: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1056:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1056:53: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame_ui/main.py:1077:18: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1103:4: W0603: Using the global statement (global-statement)
pygame_ui/main.py:1111:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
pygame_ui/main.py:1118:29: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1118:61: E1101: Module 'pygame' has no 'K_r' member (no-member)
pygame_ui/main.py:1164:4: E1101: Module 'pygame' has no 'quit' member (no-member)
pygame_ui/main.py:1099:0: R0912: Too many branches (13/12) (too-many-branches)
pygame_ui/main.py:1167:30: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1207:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1207:53: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame_ui/main.py:1228:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1228:4: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame_ui/main.py:1167:0: R0912: Too many branches (19/12) (too-many-branches)
pygame_ui/main.py:1167:0: R0915: Too many statements (54/50) (too-many-statements)
pygame_ui/main.py:46:0: C0411: standard import "random" should be placed before third party import "pygame" (wrong-import-order)
************* Module cli.cli
cli/cli.py:42:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
cli/cli.py:82:0: R0914: Too many local variables (19/15) (too-many-locals)
cli/cli.py:82:0: R0912: Too many branches (20/12) (too-many-branches)
cli/cli.py:82:0: R0915: Too many statements (71/50) (too-many-statements)
************* Module core.game
core/game.py:338:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/game.py:84:8: C2801: Unnecessarily calls dunder method __init__. Instantiate class directly. (unnecessary-dunder-call)
core/game.py:157:4: R0912: Too many branches (20/12) (too-many-branches)
core/game.py:242:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
core/game.py:323:4: R0912: Too many branches (14/12) (too-many-branches)
core/game.py:413:4: R0911: Too many return statements (7/6) (too-many-return-statements)
core/game.py:413:4: R0912: Too many branches (21/12) (too-many-branches)
core/game.py:413:4: R0915: Too many statements (54/50) (too-many-statements)
************* Module tests.test_game
tests/test_game.py:641:0: C0301: Line too long (111/100) (line-too-long)
tests/test_game.py:1:0: C0302: Too many lines in module (1178/1000) (too-many-lines)
tests/test_game.py:210:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:226:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:311:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:399:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:576:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:629:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:654:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:904:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:928:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:1096:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:1130:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:1159:8: W0612: Unused variable 'player' (unused-variable)
tests/test_game.py:13:0: R0904: Too many public methods (73/20) (too-many-public-methods)
************* Module tests.test_board
tests/test_board.py:1:0: R0801: Similar lines in 2 files
==tests.test_exceptions:[29:37]
==tests.test_game:[23:36]
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
Your code has been rated at 9.36/10


```
