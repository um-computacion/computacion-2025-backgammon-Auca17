# Automated Reports

## Coverage Report
```text
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
core/__init__.py            0      0   100%
core/board.py              98      3    97%   106-107, 171
core/checker.py            14      0   100%
core/dice.py               12      0   100%
core/game.py              159      6    96%   144-145, 165, 188, 233, 292
core/player.py             31      1    97%   39
pygame_ui/__init__.py       0      0   100%
pygame_ui/main.py         558    295    47%   241-256, 287, 301-303, 308-310, 338, 349-351, 364-381, 389-426, 431-441, 449-510, 517-616, 630-644, 676-735, 743-780, 790-829, 838-901, 918-944, 999, 1047, 1092-1093, 1107-1168, 1189-1192, 1197, 1212, 1218-1222, 1249
-----------------------------------------------------
TOTAL                     872    305    65%

```

## Pylint Report
```text
************* Module pygame_ui.main
pygame_ui/main.py:1:0: C0302: Too many lines in module (1249/1000) (too-many-lines)
pygame_ui/main.py:52:0: E1101: Module 'pygame' has no 'init' member (no-member)
pygame_ui/main.py:157:4: C0104: Disallowed name "bar" (disallowed-name)
pygame_ui/main.py:219:8: W0621: Redefining name 'i' from outer scope (line 110) (redefined-outer-name)
pygame_ui/main.py:261:4: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame_ui/main.py:261:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:261:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:261:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:230:0: R0912: Too many branches (31/12) (too-many-branches)
pygame_ui/main.py:230:0: R0915: Too many statements (53/50) (too-many-statements)
pygame_ui/main.py:261:4: R1702: Too many nested blocks (8/5) (too-many-nested-blocks)
pygame_ui/main.py:398:8: W0621: Redefining name 'i' from outer scope (line 110) (redefined-outer-name)
pygame_ui/main.py:444:0: R0914: Too many local variables (27/15) (too-many-locals)
pygame_ui/main.py:467:8: W0621: Redefining name 'i' from outer scope (line 110) (redefined-outer-name)
pygame_ui/main.py:457:4: W0612: Unused variable 'shadow_color' (unused-variable)
pygame_ui/main.py:513:0: R0914: Too many local variables (28/15) (too-many-locals)
pygame_ui/main.py:527:12: W0621: Redefining name 'i' from outer scope (line 110) (redefined-outer-name)
pygame_ui/main.py:518:4: C0104: Disallowed name "bar" (disallowed-name)
pygame_ui/main.py:653:0: R0914: Too many local variables (16/15) (too-many-locals)
pygame_ui/main.py:785:0: R0914: Too many local variables (17/15) (too-many-locals)
pygame_ui/main.py:835:0: R0914: Too many local variables (21/15) (too-many-locals)
pygame_ui/main.py:954:4: C0103: Variable name "A" doesn't conform to snake_case naming style (invalid-name)
pygame_ui/main.py:995:8: W0621: Redefining name 'i' from outer scope (line 110) (redefined-outer-name)
pygame_ui/main.py:981:7: W0612: Unused variable 'y' (unused-variable)
pygame_ui/main.py:1002:30: W0621: Redefining name 'game_data' from outer scope (line 183) (redefined-outer-name)
pygame_ui/main.py:1004:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1013:36: W0621: Redefining name 'game_data' from outer scope (line 183) (redefined-outer-name)
pygame_ui/main.py:1015:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1042:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1046:24: E1101: Module 'pygame' has no 'K_BACKSPACE' member (no-member)
pygame_ui/main.py:1055:36: W0621: Redefining name 'game_data' from outer scope (line 183) (redefined-outer-name)
pygame_ui/main.py:1057:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1057:53: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame_ui/main.py:1080:18: W0621: Redefining name 'game_data' from outer scope (line 183) (redefined-outer-name)
pygame_ui/main.py:1106:4: W0603: Using the global statement (global-statement)
pygame_ui/main.py:1114:29: E1101: Module 'pygame' has no 'QUIT' member (no-member)
pygame_ui/main.py:1121:29: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1121:61: E1101: Module 'pygame' has no 'K_r' member (no-member)
pygame_ui/main.py:1167:4: E1101: Module 'pygame' has no 'quit' member (no-member)
pygame_ui/main.py:1102:0: R0912: Too many branches (13/12) (too-many-branches)
pygame_ui/main.py:1171:30: W0621: Redefining name 'game_data' from outer scope (line 183) (redefined-outer-name)
pygame_ui/main.py:1173:21: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame_ui/main.py:1173:53: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame_ui/main.py:1194:21: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame_ui/main.py:1194:4: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame_ui/main.py:1171:0: R0912: Too many branches (19/12) (too-many-branches)
pygame_ui/main.py:1171:0: R0915: Too many statements (54/50) (too-many-statements)
pygame_ui/main.py:46:0: C0411: standard import "sys" should be placed before third party import "pygame" (wrong-import-order)
pygame_ui/main.py:47:0: C0411: standard import "random" should be placed before third party import "pygame" (wrong-import-order)
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
************* Module tests.test_ui
tests/test_ui.py:49:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:52:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:55:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:66:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:69:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:72:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:111:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:122:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:127:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:131:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:143:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:145:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:147:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:165:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:179:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:181:36: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:182:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:224:0: C0301: Line too long (117/100) (line-too-long)
tests/test_ui.py:238:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:239:0: C0301: Line too long (107/100) (line-too-long)
tests/test_ui.py:240:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:242:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:252:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:254:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:264:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:266:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:280:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:285:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:300:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_ui.py:323:0: W0311: Bad indentation. Found 13 spaces, expected 12 (bad-indentation)
tests/test_ui.py:324:0: W0311: Bad indentation. Found 13 spaces, expected 12 (bad-indentation)
tests/test_ui.py:347:0: W0311: Bad indentation. Found 13 spaces, expected 12 (bad-indentation)
tests/test_ui.py:348:0: W0311: Bad indentation. Found 13 spaces, expected 12 (bad-indentation)
tests/test_ui.py:19:0: C0413: Import "from pygame_ui import main" should be placed at the top of the module (wrong-import-position)
tests/test_ui.py:32:8: E1101: Module 'pygame' has no 'init' member (no-member)
tests/test_ui.py:33:40: E1101: Module 'pygame' has no 'NOFRAME' member (no-member)
tests/test_ui.py:39:8: E1101: Module 'pygame' has no 'quit' member (no-member)
tests/test_ui.py:51:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:68:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:89:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:108:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:125:40: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:129:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:129:68: E1101: Module 'pygame' has no 'K_a' member (no-member)
tests/test_ui.py:144:40: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:144:64: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:162:46: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:167:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:167:68: E1101: Module 'pygame' has no 'K_a' member (no-member)
tests/test_ui.py:159:8: W0612: Unused variable 'initial_state' (unused-variable)
tests/test_ui.py:184:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:202:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:225:44: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:283:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:283:68: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:302:44: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
tests/test_ui.py:302:68: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
tests/test_ui.py:323:45: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
tests/test_ui.py:347:45: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
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
************* Module tests.test_logic
tests/test_logic.py:129:0: C0303: Trailing whitespace (trailing-whitespace)
tests/test_logic.py:16:0: C0413: Import "from pygame_ui import main" should be placed at the top of the module (wrong-import-position)
tests/test_logic.py:1:0: R0801: Similar lines in 2 files
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
        ) (duplicate-code)

-----------------------------------
Your code has been rated at 8.16/10


```
