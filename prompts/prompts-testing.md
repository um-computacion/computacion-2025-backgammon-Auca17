# Registro de Prompts de Testing

## Prompt #1: Creación de Tests para Game

**Modelo/herramienta usada:** GitHub Copilot (junio 2024)

**Texto exacto del prompt:**

Bien ahora dentro de test_game, haz tests para game. documenta en que consiste cada test, y dentro de prompts-desarrollo sigue las instrucciones

**Instrucciones del sistema:**

- Siempre sigue los principios SOLID
- Incluir docstrings y comentarios claros en el código generado
- Proporciona una explicación detallada para cada prompt y documenta tanto el prompt como la respuesta generada dentro de los archivos prompts-desarrollo.md, prompts/prompts-documentacion.md o prompts/prompts-testing.md. Usa únicamente estos archivos para la documentación de prompts.
- Por cada prompt debe quedar registrado: Modelo / herramienta usada (nombre y versión si corresponde), El texto exacto del prompt (sin reescrituras subjetivas), Instrucciones del sistema (si las hubo), Respuesta/resultado completo devuelto por la IA, Indicar si la salida fue usada sin cambios, usada con modificaciones (mostrar las modificaciones) o descartada, Referencia a los archivos finales que incorporaron contenido generado por IA (ej:core/board.py)

**Respuesta/resultado completo devuelto por la IA:**

---

Para crear pruebas unitarias para la clase Game en test_game.py, se utilizó el módulo unittest de Python. Las pruebas cubren aspectos clave como inicialización, gestión de turnos, movimientos válidos e inválidos, y verificación de estado del juego. Cada test incluye docstrings que explican su propósito y lógica.

**Proceso de generación:**

1. Importar unittest y las clases necesarias (Game, Player, Board).
2. Crear una clase TestGame que herede de unittest.TestCase.
3. Usar setUp para inicializar objetos comunes.
4. Definir métodos de prueba para cada funcionalidad, con aserciones para verificar el comportamiento esperado.
5. Incluir docstrings en cada método de prueba explicando qué se verifica.

Código generado:

```python
import unittest
from core.game import Game
from core.player import Player
from core.board import Board

class TestGame(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Game.
    Cada método de prueba verifica un aspecto específico del comportamiento del juego.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        Crea dos jugadores y un juego para usar en las pruebas.
        """
        self.player1 = Player("Alice", "white", [])
        self.player2 = Player("Bob", "black", [])
        self.game = Game(self.player1, self.player2)

    def test_initialization(self):
        """
        Verifica que el juego se inicialice correctamente con dos jugadores,
        un tablero vacío, turno inicial en 0 y sin ganador.
        """
        self.assertIsInstance(self.game._Game__board__, Board)
        self.assertEqual(len(self.game._Game__players__), 2)
        self.assertEqual(self.game._Game__current_turn__, 0)
        self.assertIsNone(self.game._Game__winner__)

    def test_switch_turn(self):
        """
        Verifica que el turno cambie correctamente entre los dos jugadores.
        """
        self.assertEqual(self.game._Game__current_turn__, 0)
        self.game.switch_turn()
        self.assertEqual(self.game._Game__current_turn__, 1)
        self.game.switch_turn()
        self.assertEqual(self.game._Game__current_turn__, 0)

    def test_get_current_player(self):
        """
        Verifica que se devuelva el jugador correcto según el turno actual.
        """
        self.assertEqual(self.game.get_current_player(), self.player1)
        self.game.switch_turn()
        self.assertEqual(self.game.get_current_player(), self.player2)

    def test_is_over_and_get_winner(self):
        """
        Verifica que el juego no esté terminado inicialmente y que no haya ganador.
        """
        self.assertFalse(self.game.is_over())
        self.assertIsNone(self.game.get_winner())

    def test_make_move_valid(self):
        """
        Verifica que un movimiento válido se ejecute correctamente.
        Asume una configuración simplificada donde el tablero permite movimientos adyacentes.
        """
        # Configurar tablero para un movimiento válido (simplificado)
        self.game._Game__board__._Board__points = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = self.game.make_move(self.player1, 0, 1)
        self.assertTrue(result)
        self.assertEqual(self.game._Game__board__._Board__points[0], 0)
        self.assertEqual(self.game._Game__board__._Board__points[1], 1)

    def test_make_move_invalid_out_of_bounds(self):
        """
        Verifica que un movimiento fuera de los límites del tablero sea rechazado.
        """
        result = self.game.make_move(self.player1, -1, 0)
        self.assertFalse(result)
        result = self.game.make_move(self.player1, 0, 24)
        self.assertFalse(result)

    def test_make_move_invalid_no_checker(self):
        """
        Verifica que un movimiento sea rechazado si no hay ficha del jugador en la posición de origen.
        """
        result = self.game.make_move(self.player1, 0, 1)
        self.assertFalse(result)

    def test_make_move_invalid_landing_on_opponent(self):
        """
        Verifica que un movimiento sea rechazado si intenta aterrizar en una posición ocupada por el oponente.
        """
        # Configurar tablero con oponente en posición 1
        self.game._Game__board__._Board__points = [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = self.game.make_move(self.player1, 0, 1)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
```

**Comentarios:**

- Las pruebas siguen los principios SOLID, enfocándose en una responsabilidad por test.
- Se incluyen docstrings detalladas para cada test, explicando su propósito.
- El código generado es confiable y facilita la detección de errores en la clase Game.

**Estado de la salida:** Usado sin cambios.

**Referencia a archivos finales:** tests/test_game.py

---

## Prompt #2: Creación de Tests para Player

**Modelo/herramienta usada:** GitHub Copilot (junio 2024)

**Texto exacto del prompt:**

Bien ahora dentro de test_player, haz tests para player.py. documenta en que consiste cada test, y dentro de prompts-desarrollo , sigue las instrucciones que se encuentra en copilot-instruccions

**Instrucciones del sistema:**

- Siempre sigue los principios SOLID
- Incluir docstrings y comentarios claros en el código generado
- Proporciona una explicación detallada para cada prompt y documenta tanto el prompt como la respuesta generada dentro de los archivos prompts-desarrollo.md, prompts/prompts-documentacion.md o prompts/prompts-testing.md. Usa únicamente estos archivos para la documentación de prompts.
- Por cada prompt debe quedar registrado: Modelo / herramienta usada (nombre y versión si corresponde), El texto exacto del prompt (sin reescrituras subjetivas), Instrucciones del sistema (si las hubo), Respuesta/resultado completo devuelto por la IA, Indicar si la salida fue usada sin cambios, usada con modificaciones (mostrar las modificaciones) o descartada, Referencia a los archivos finales que incorporaron contenido generado por IA (ej:core/board.py)

**Respuesta/resultado completo devuelto por la IA:**

---

Para crear pruebas unitarias para la clase Player en test_player.py, se utilizó el módulo unittest de Python. Las pruebas cubren aspectos clave como inicialización, gestión de fichas (checkers), y validaciones básicas. Cada test incluye docstrings que explican su propósito y lógica.

**Proceso de generación:**

1. Importar unittest y la clase Player.
2. Crear una clase TestPlayer que herede de unittest.TestCase.
3. Usar setUp para inicializar un objeto Player común.
4. Definir métodos de prueba para cada funcionalidad, con aserciones para verificar el comportamiento esperado.
5. Incluir docstrings en cada método de prueba explicando qué se verifica.

Código generado:

```python
import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Player.
    Cada método de prueba verifica un aspecto específico del comportamiento del jugador.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        Crea un jugador para usar en las pruebas.
        """
        self.player = Player("Alice", "white", [])

    def test_initialization(self):
        """
        Verifica que el jugador se inicialice correctamente con nombre, color y lista de fichas vacía.
        """
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(self.player.color, "white")
        self.assertEqual(self.player.checkers, [])

    def test_add_checker(self):
        """
        Verifica que se pueda agregar una ficha a la lista de fichas del jugador.
        """
        self.player.add_checker(1)
        self.assertIn(1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 1)

    def test_remove_checker(self):
        """
        Verifica que se pueda remover una ficha existente de la lista de fichas del jugador.
        """
        self.player.add_checker(1)
        self.player.remove_checker(1)
        self.assertNotIn(1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 0)

    def test_remove_checker_not_present(self):
        """
        Verifica que intentar remover una ficha no presente no cause errores y no modifique la lista.
        """
        initial_length = len(self.player.checkers)
        self.player.remove_checker(1)  # Ficha no presente
        self.assertEqual(len(self.player.checkers), initial_length)

    def test_get_checker_count(self):
        """
        Verifica que se devuelva correctamente el número de fichas del jugador.
        """
        self.assertEqual(self.player.get_checker_count(), 0)
        self.player.add_checker(1)
        self.player.add_checker(2)
        self.assertEqual(self.player.get_checker_count(), 2)

if __name__ == '__main__':
    unittest.main()
```

**Comentarios:**

- Las pruebas siguen los principios SOLID, enfocándose en una responsabilidad por test.
- Se incluyen docstrings detalladas para cada test, explicando su propósito.
- El código generado es confiable y facilita la detección de errores en la clase Player.

**Estado de la salida:** Usado sin cambios.

**Referencia a archivos finales:** tests/test_player.py

---

## Prompt #3: Implementar y Verificar la Regla de Dobles

**Modelo/herramienta usada:** GitHub Copilot - Herramientas: read_file, set_plan, replace_with_git_merge_diff, run_in_bash_session, submit

**Texto exacto del prompt:**

El primer objetivo es que cuando el jugador saca doble, se deberia poder mover 4 veces, no 2. Ademas, crea un test para eso

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Tras revisar core/game.py, descubrí que la lógica para manejar dobles (otorgando 4 movimientos) ya estaba implementada correctamente.

Por lo tanto, el plan se centró en crear un test de verificación para confirmar esta funcionalidad.

**Acciones realizadas:**

- Añadí un nuevo test, test_roll_dice_doubles, en tests/test_game.py.
- Este test utiliza unittest.mock.patch para simular una tirada de dados que resulta en un doble (ej: 3-3).
- El test verifica que, después de la tirada, la lista de valores de dados en la instancia del juego sea [3, 3, 3, 3].
- Ejecuté todas las pruebas y, al confirmarse que pasaban, envié el cambio.

Código generado (adición en tests/test_game.py):

```python
# Este bloque fue añadido a la clase TestGame en tests/test_game.py

@patch('core.dice.Dice.roll')
def test_roll_dice_doubles(self, __mock_roll__):
    """
    Verifica que si se saca un doble, se obtienen 4 movimientos.
    """
    # Simulamos que los dados siempre sacan (3, 3)
    self.__game__.__dice__.get_values = lambda: (3, 3)
    self.__game__.__dice__.is_double = lambda: True
    
    # Llamamos al método que tira los dados
    self.__game__.roll_dice()
    
    # Verificamos que los valores de los dados son cuatro 3s
    self.assertEqual(self.__game__.__dice_values__, [3, 3, 3, 3])
```

**Estado de la salida:** Usada con modificaciones. El plan inicial era "implementar y testear", pero se modificó a "solo testear" al descubrir que el código ya existía. El código del test fue una adición neta.

**Referencia a archivos finales:** tests/test_game.py

---

## Prompt #4: Implementación del Refactor SOLID (Testing Relevante)

**Modelo/herramienta usada:** GitHub Copilot - Herramientas: read_file, replace_with_git_merge_diff, run_in_bash_session, submit

**Texto exacto del prompt:**

(Implícito, siguiendo el plan de refactorización)

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Durante la refactorización, se actualizaron los archivos de pruebas para adaptarse a la nueva inyección de dependencias (DIP).

**Acciones realizadas:**

- En tests/test_game.py y tests/test_exceptions.py, se ajustaron los métodos setUp para crear instancias de Board y Dice y pasarlas al constructor de Game.
- Después de cada refactor, se ejecutó la suite completa de tests (python3 -m unittest discover tests) confirmando que ninguna funcionalidad fue rota.

Código generado (fragmento clave en tests/test_game.py):

def setUp(self):
    self.board = Board()
    self.dice = Dice()
    self.player1 = Player("A", "white")
    self.player2 = Player("B", "black")
    self.game = Game(self.player1, self.player2, self.board, self.dice)

**Estado de la salida:** Usada sin cambios. Las modificaciones de prueba garantizaron la compatibilidad del refactor SOLID.

**Referencia a archivos finales:** tests/test_game.py, tests/test_exceptions.py

---

## Prompt #5: Corrección del Bug Visual (Testing Asociado)

**Modelo/herramienta usada:** GitHub Copilot - Herramientas: replace_with_git_merge_diff, run_in_bash_session, submit

**Texto exacto del prompt:**

(Implícito, siguiendo el plan de corrección de bug)

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Tras ajustar el espaciado del método get_2d_representation en core/board.py, se actualizó el test test_get_2d_representation en tests/test_board.py.

**Acciones realizadas:**

- El string esperado se alineó con la nueva salida visual.
- La suite completa de pruebas se ejecutó y pasó satisfactoriamente.

Código generado (fragmento conceptual):

```python
# Actualización en tests/test_board.py
expected_output = """
12 13 14 15 16 17   18 19 20 21 22 23
...
"""
self.assertEqual(board.get_2d_representation().strip(), expected_output.strip())
```

**Estado de la salida:** Usada con modificaciones. El primer intento de corrección fue descartado, el segundo fue definitivo y validado por tests actualizados.

**Referencia a archivos finales:** core/board.py, tests/test_board.py

---

## Prompt #6: Implementación (con Bug) y Corrección del Bug Crítico

**Modelo/herramienta usada:** GitHub Copilot - Herramientas: read_file, replace_with_git_merge_diff, run_in_bash_session, request_code_review, submit

**Texto exacto del prompt:**

(Implícito, siguiendo el plan y la corrección posterior a la revisión de código)

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Durante la primera implementación de la nueva secuencia de inicio, se introdujo un bug al pasar un índice de jugador donde se esperaba un color ('X' o 'O').

**Acciones realizadas:**

- La herramienta de revisión de código detectó la inconsistencia.
- Se corrigió el método _decide_first_player en cli/cli.py para devolver el color correcto y se ajustó la llamada a set_initial_turn en core/game.py.
- Se verificó que todas las pruebas (test_game.py y test_excepciones.py) pasaran correctamente y la aplicación fuera coherente.

Código generado (versión corregida):

```python
# cli/cli.py
def _decide_first_player(player1_name, player2_name):
    # ...
    if d1 > d2:
        return 'O', [d1, d2]
    elif d2 > d1:
        return 'X', [d1, d2]

# core/game.py
def set_initial_turn(self, initial_data):
    player_color, dice_values = initial_data
    # ... lógica final corregida ...
```

**Estado de la salida:** Usada con modificaciones críticas. La primera versión fue descartada; la segunda se adoptó tras revisión de código.

**Referencia a archivos finales:** cli/cli.py, core/game.py, tests/test_game.py, tests/test_exceptions.py

---

## Prompt #7: Creación del Archivo de Test para el CLI

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, siguiendo el plan aprobado).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se creó el archivo inicial de pruebas para la interfaz de línea de comandos (CLI).

Código generado (fragmento inicial):

```python
import unittest
from unittest.mock import patch, call
from io import StringIO
import sys

from cli.cli import main

class TestCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["Player1", "Player2", "salir"])
    @patch("sys.stdout", new_callable=StringIO)
    @patch("random.randint", return_value=3)  # Para evitar bucles infinitos en el desempate
    def test_main_loop_exit(self, mock_randint, mock_stdout, mock_input):
        """Prueba que el bucle principal termina cuando el usuario escribe 'salir'."""
        main()
        self.assertIn("Juego terminado.", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()
```

**Estado de la salida:** Usada con modificaciones (el archivo se extendió posteriormente).

**Referencia a archivos finales:** tests/test_cli.py

---

## Prompt #8: Cobertura de core/exceptions.py

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, siguiendo el plan aprobado).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se añadió un test para verificar la instanciación de las excepciones personalizadas del módulo core/exceptions.py.

Código generado (adición en tests/test_exceptions.py):

```python
# tests/test_exceptions.py (método añadido en la clase TestExceptions)
def test_custom_exceptions_instantiation(self):
    """Verifica que las excepciones personalizadas se pueden instanciar."""
    self.assertIsInstance(InvalidMoveError(), InvalidMoveError)
    self.assertIsInstance(InvalidTurnError(), InvalidTurnError)
    self.assertIsInstance(GameOverError(), GameOverError)
    self.assertIsInstance(GameNotStartedError(), GameNotStartedError)
```

**Estado de la salida:** Usada sin cambios.

Referencia a archivos finales: tests/test_exceptions.py

---

## Prompt #9: Cobertura de Líneas Faltantes en core/board.py

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, para cubrir líneas 105-106 y 170 según coverage).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se añadieron tests para cubrir las líneas faltantes en core/board.py según el reporte de cobertura.

Código generado (adiciones en tests/test_board.py):

```python
# tests/test_board.py (métodos añadidos en la clase TestBoard)

def test_checker_repr_no_owner(self):
    """Prueba la representación de un checker sin dueño."""
    checker = Checker("white", 1)
    checker.owner = None
    self.assertEqual(repr(checker), "Checker(color=white, owner=None)")

def test_bar_setters(self):
    """Prueba los setters para las fichas en la barra."""
    initial_white = self.board.white_bar
    initial_black = self.board.black_bar
    self.board.white_bar = 5
    self.board.black_bar = 3
    self.assertEqual(self.board.white_bar, 5)
    self.assertEqual(self.board.black_bar, 3)
    # Restauramos los originales
    self.board.white_bar = initial_white
    self.board.black_bar = initial_black
```

**Estado de la salida:** Usada sin cambios.

**Referencia a archivos finales:** tests/test_board.py

---

## Prompt #10: Cobertura de Líneas Faltantes en core/game.py

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, para cubrir líneas 144-145, 165, 188, 233, 292 según coverage).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se añadieron tests para cubrir las líneas faltantes en core/game.py según el reporte de cobertura.

Código generado (adiciones en tests/test_game.py):

```python
# tests/test_game.py (métodos añadidos en la clase TestGame)

def test_game_over_winner(self):
    """Prueba la condición de victoria del juego."""
    # Simulamos que el jugador 1 ha retirado todas sus fichas
    self.game.players[0].home_checkers = 15
    self.assertTrue(self.game.is_over())
    self.assertEqual(self.game.get_winner(), self.game.players[0])

def test_no_possible_moves(self):
    """Prueba el caso en el que no hay movimientos posibles."""
    # Tablero bloqueado y tirada de dados
    self.game.board.points[0] = [Checker("white", 0)]
    self.game.board.points[6] = [Checker("black", 6)] * 2
    self.game.dice_values = [6]  # Solo se puede mover de 0 a 6
    self.game.current_turn = 0   # Turno del jugador blanco

    moves = self.game.get_possible_moves()
    self.assertEqual(len(moves), 0)
```

**Estado de la salida:** Usada sin cambios.

**Referencia a archivos finales:** tests/test_game.py

---

## Prompt #11: Cobertura de Línea Faltante en core/player.py

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, para cubrir la línea 39 según coverage).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se añadió un test para cubrir la línea faltante en core/player.py según el reporte de cobertura.

Código generado (adición en tests/test_player.py):

```python
# tests/test_player.py (método añadido en la clase TestPlayer)

def test_add_bar_checker_no_checker_object(self):
    """Prueba añadir una ficha a la barra sin pasar el objeto checker."""
    initial_bar_checkers = self.player.get_bar_checkers()
    self.player.add_bar_checker()  # Llamada sin argumento
    self.assertEqual(self.player.get_bar_checkers(), initial_bar_checkers + 1)
```

**Estado de la salida:** Usada sin cambios.

**Referencia a archivos finales:** tests/test_player.py

---

## Prompt #12: Recreación Final de tests/test_cli.py (Post-Reset)

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

(Implícito, consecuencia de reset_all).

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

Se recreó el archivo completo de pruebas para el CLI tras el reset del proyecto, con cobertura completa de funcionalidades.

Código generado (fragmento representativo):

```python
# tests/test_cli.py (versión final completa)
import unittest
from unittest.mock import patch, call, MagicMock
from io import StringIO
from cli.cli import main, _get_player_names, _decide_first_player

class TestCLI(unittest.TestCase):
    """Tests para la interfaz de línea de comandos."""

    @patch("random.randint", side_effect=[6, 3])
    @patch("builtins.input", side_effect=["Alice", "Bob"])
    def test_decide_first_player_p1_wins(self, mock_input, mock_randint):
        """Prueba que el jugador 1 gana la tirada inicial."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            winner_color, _ = _decide_first_player("Alice", "Bob")
            self.assertEqual(winner_color, "O")
            self.assertIn("¡Alice empieza!", mock_stdout.getvalue())

    @patch("cli.cli.Game")
    @patch("builtins.input", side_effect=["P1", "P2", "", "salir"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_game_exit(self, mock_stdout, mock_input, mock_game_cls):
        """Prueba el flujo principal y la salida del juego."""
        main()
        self.assertIn("Juego terminado.", mock_stdout.getvalue())
```

**Estado de la salida:** Usada sin cambios (versión final del archivo).

**Referencia a archivos finales:** tests/test_cli.py

---
