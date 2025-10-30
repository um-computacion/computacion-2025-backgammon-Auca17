# Automated Reports

## Coverage Report

```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cli/__init__.py          0      0   100%
cli/cli.py              79     79     0%   5-133
core/__init__.py         0      0   100%
core/board.py           98      3    97%   105-106, 170
core/checker.py         12      0   100%
core/dice.py            12      0   100%
core/exceptions.py       5      5     0%   6-22
core/game.py           159      6    96%   144-145, 165, 188, 233, 292
core/player.py          31      1    97%   39
--------------------------------------------------
TOTAL                  396     94    76%

```

## Pylint Report

```text
************* Module pygame_ui.main
pygame_ui/main.py:1167:0: C0303: Trailing whitespace (trailing-whitespace)
pygame_ui/main.py:1:0: C0302: Too many lines in module (1284/1000) (too-many-lines)
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
pygame_ui/main.py:1168:30: W0621: Redefining name 'game_data' from outer scope (line 182) (redefined-outer-name)
pygame_ui/main.py:1208:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1208:53: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame_ui/main.py:1229:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1229:4: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame_ui/main.py:1168:0: R0912: Too many branches (19/12) (too-many-branches)
pygame_ui/main.py:1168:0: R0915: Too many statements (54/50) (too-many-statements)
pygame_ui/main.py:46:0: C0411: standard import "random" should be placed before third party import "pygame" (wrong-import-order)
************* Module cli.cli
cli/cli.py:93:0: C0301: Line too long (116/100) (line-too-long)
cli/cli.py:38:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
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
core/board.py:10:0: C0301: Line too long (107/100) (line-too-long)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:13:23: W0622: Redefining built-in '__name__' (redefined-builtin)
************* Module core.dice
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module tests.test_checker
tests/test_checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_checker.py:4:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_ui
tests/test_ui.py:28:8: E1101: Module 'pygame' has no 'init' member (no-member)
tests/test_ui.py:29:40: E1101: Module 'pygame' has no 'NOFRAME' member (no-member)
tests/test_ui.py:35:8: E1101: Module 'pygame' has no 'quit' member (no-member)
tests/test_ui.py:48:12: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:66:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:88:12: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:109:12: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:127:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:132:12: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:132:36: E1101: Module 'pygame' has no 'K_a' member (no-member)
tests/test_ui.py:148:40: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:148:64: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:169:12: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:177:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:177:68: E1101: Module 'pygame' has no 'K_a' member (no-member)
tests/test_ui.py:165:8: W0612: Unused variable 'initial_state' (unused-variable)
tests/test_ui.py:198:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:220:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:247:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:312:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:312:68: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:335:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:335:68: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:360:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:388:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
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
tests/test_board.py:8:0: C0115: Missing class docstring (missing-class-docstring)
************* Module tests.test_logic
tests/test_logic.py:1:0: R0801: Similar lines in 2 files
==tests.test_exceptions:[19:29]
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
        ) (duplicate-code)

-----------------------------------
Your code has been rated at 8.38/10


```
