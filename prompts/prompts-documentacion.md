# Registro de Prompts de Documentación

## Prompt #1: Generación de Diagrama de Clases UML en Mermaid para carpeta Core

**Modelo/herramienta usada:** GitHub Copilot (Claude Sonnet 4.5)

**Texto exacto del prompt:**
```
generar un diagrama de clases UML para Core
```

**Instrucciones del sistema:**

- Siempre seguir los principios SOLID
- Incluir docstrings y comentarios claros en el código generado
- Proporcionar explicación detallada para cada prompt
- Documentar cada prompt en `prompts-desarrollo.md`, `prompts-documentacion.md` o `prompts-testing.md`
- Registrar: modelo usado, texto exacto del prompt, instrucciones del sistema, respuesta completa, estado de uso, archivos afectados

**Contexto:**

El usuario solicitó un diagrama de clases UML en formato Mermaid que represente todas las clases del paquete `core/` del proyecto Backgammon. Se adjuntó el archivo `dice.py` como referencia activa y un diagrama previo existente.

**Archivos analizados:**

- `core/board.py` - Clase Board (gestión del tablero)
- `core/checker.py` - Clase Checker (fichas)
- `core/dice.py` - Clase Dice (dados)
- `core/game.py` - Clase Game (controlador principal)
- `core/player.py` - Clase Player (jugadores)
- `core/exceptions.py` - Excepciones personalizadas

**Respuesta/resultado completo devuelto por la IA:**

---

## Diagrama de clases - carpeta /core

```mermaid
classDiagram
    %% Clase Game - Controlador principal del juego
    class Game {
        -Board __board__
        -List~Player~ __players__
        -Dice __dice__
        -int __current_turn__
        -List~int~ __dice_values__
        -Player __winner__
        +__init__(player1: Player, player2: Player, board: Board, dice: Dice)
        +start() void
        +roll_dice() void
        +make_move(from_pos: int, to_pos: int) bool
        +switch_turn() void
        +get_current_player() Player
        +get_dice_values() List~int~
        +get_possible_moves() List~str~
        +is_over() bool
        +get_winner() Player
        +display_board() void
        +reset() void
        -_validate_move(player: Player, from_pos: int, to_pos: int, die: int) bool
        -_validate_reentry(player: Player, to_pos: int, die: int) bool
        -_validate_bear_off(player: Player, from_pos: int, die: int) bool
        -_can_bear_off(player: Player) bool
        -_execute_move(player: Player, from_pos: int, to_pos: int) void
        -_execute_reentry(player: Player, to_pos: int) void
        -_execute_bear_off(player: Player, from_pos: int) void
    }

    %% Clase Board - Representa el tablero
    class Board {
        -List~Dict~ __points_status__
        -Dict~str, List~ __bar__
        -Dict~str, int~ __off__
        +__init__()
        +get_point(point: int) Dict
        +move_checker(color: str, from_point: int, to_point: int) bool
        +bear_off_checker(color: str, from_point: int) bool
        +enter_from_captured(color: str, to_point: int) bool
        +get_bar() Dict~str, List~
        +get_off() Dict~str, int~
        +get_home(color: str) List~int~
        +get_2d_representation() str
        +display() void
    }

    %% Clase Player - Representa un jugador
    class Player {
        -str __name__
        -str __color__
        -int __checkers_off__
        +__init__(player_name: str, color: str)
        +get_name() str
        +get_color() str
        +get_checkers_off() int
        +increment_checkers_off() void
        +reset_checkers_off() void
    }

    %% Clase Dice - Representa los dados
    class Dice {
        -int __value1__
        -int __value2__
        +__init__()
        +roll() void
        +get_values() Tuple~int, int~
        +is_double() bool
    }

    %% Clase Checker - Representa una ficha
    class Checker {
        -str __color__
        +__init__(color: str)
        +get_color() str
        +__str__() str
    }

    %% Enumeraciones de excepciones personalizadas
    class InvalidMoveException {
        <<exception>>
    }

    class InvalidReentryException {
        <<exception>>
    }

    class InvalidBearOffException {
        <<exception>>
    }

    %% Relaciones de composición y agregación
    Game "1" *-- "1" Board : contiene
    Game "1" *-- "2" Player : contiene
    Game "1" *-- "1" Dice : contiene
    Board "1" o-- "*" Checker : gestiona
    Player "1" -- "1" Checker : tiene color

    %% Relaciones de uso (dependencias)
    Game ..> InvalidMoveException : lanza
    Game ..> InvalidReentryException : lanza
    Game ..> InvalidBearOffException : lanza

    %% Notas sobre responsabilidades
    note for Game "Controlador principal: gestiona turnos,\nmovimientos, validaciones y fin del juego"
    note for Board "Gestiona estado del tablero:\nposiciones, barra y bear-off"
    note for Player "Representa un jugador:\nnombre, color y progreso"
    note for Dice "Gestiona tiradas de dados\ny detección de dobles"
    note for Checker "Representa una ficha individual\ncon su color"
```

**Estado de la salida:** ✅ Usado sin cambios

El diagrama generado fue aceptado completamente sin modificaciones.

**Referencia a archivos finales:** `docs/diagrams/core-class-diagram.md`

---

## Prompt #2: Modificación para Subir Calidad de Pylint

**Modelo/herramienta usada:** Jules

**Texto exacto del prompt:**

Quiero subir mi calidad de codigo segun pylint dime cual es el error y luego la solucion para ir aprendiendo

**Instrucciones del sistema:**

No se especificaron instrucciones adicionales.

**Respuesta/resultado completo devuelto por la IA:**

---

### Desglose Detallado de las Correcciones de Pylint

Hola, aquí tienes el informe detallado sobre los cambios específicos que realicé para aumentar la puntuación de Pylint a 9.57/10. Entiendo que mis mensajes anteriores no llegaban correctamente, así que he creado este archivo para presentarte la información de forma clara.

#### 1. El Cambio más Impactante: redefined-builtin (W0622)

**Problema:** Pylint se quejaba de que estábamos usando la palabra `name` como un nombre de atributo en la clase Player. Esto es una mala práctica porque `name` puede chocar con funciones o palabras clave incorporadas en Python.

**Solución:** Renombrar el atributo `name` a `player_name` en toda la base de código.

Código ANTES (core/player.py):

```python
class Player:
    def __init__(self, name, color, checkers=None):
        self.name = name  # <-- PYLINT ERROR AQUÍ
        # ...
    def get_name(self):
        return self.name # <-- Y AQUÍ
```

Código DESPUÉS (core/player.py):

```python
class Player:
    def __init__(self, player_name, color, checkers=None):
        self.player_name = player_name # <-- Corregido
        # ...
    def get_player_name(self):
        """Devuelve el nombre del jugador."""
        return self.player_name # <-- Corregido
```

**Archivos afectados:** core/player.py, cli/cli.py, tests/test_game.py, tests/test_player.py

#### 2. Corrección Estructural: unnecessary-dunder-call (W0124)

**Problema:** Pylint detectó que en el método `reset()` de la clase Game, se estaba llamando directamente a `self.__init__()`. Esto no es idiomático en Python y puede tener efectos secundarios no deseados.

**Solución:** En lugar de llamar a `__init__`, se re-inicializaron manualmente los atributos del estado del juego a sus valores por defecto.

Código ANTES (core/game.py):

```python
def reset(self):
    """Resetea el juego a su estado inicial."""
    # Llamar a __init__ para restablecer el estado.
    self.__init__(self.players[0], self.players[1], self.board, self.dice) # <-- PYLINT ERROR
```

Código DESPUÉS (core/game.py):

```python
def reset(self):
    """Resetea el juego a su estado inicial."""
    # Re-inicializa los atributos del estado en lugar de llamar a __init__
    self.current_turn = 0
    self.dice_values = []
    self.is_started = False
    self.winner = None
    self.board.setup_board()  # Se resetea el tablero por separado
```

**Archivos afectados:** core/game.py

#### 3. Limpieza y Documentación: missing-docstring (C0114, C0115, C0116)

**Problema:** Una gran cantidad de puntos se perdían porque los módulos, clases y métodos no tenían docstrings (cadenas de documentación).

**Solución:** Añadir docstrings descriptivos en todos los lugares donde faltaban.

Código ANTES (core/dice.py):

```python
import random

class Dice:
    def __init__(self):
        self.values = (0, 0)
```

Código DESPUÉS (core/dice.py):

```python
"""
Este módulo contiene la implementación de los dados del Backgammon.
"""
import random

class Dice:
    """Representa un par de dados para el juego."""
    def __init__(self):
        """Inicializa los dados con valores a cero."""
        self.values = (0, 0)
```

**Archivos afectados:** Prácticamente todos los archivos .py

#### 4. Pruebas más Limpias: unused-argument (W0613)

**Problema:** En los archivos de test, es muy común que los argumentos de los mocks (`mock_input`, `mock_stdout`, etc.) no se usen directamente en el cuerpo de la función de prueba, lo cual genera una advertencia en Pylint.

**Solución:** Renombrar los argumentos no utilizados añadiéndoles un prefijo de guion bajo (`_`). Esto es una convención estándar para indicar a Pylint (y a otros programadores) que el argumento es intencionadamente no utilizado.

Código ANTES (tests/test_cli.py):

```python
@patch("sys.stdout", new_callable=StringIO)
def test_main_game_exit(self, mock_stdout, mock_input, mock_game_cls): #<-- ERROR AQUÍ
    """Prueba el flujo principal y la salida del juego."""
    main()
    # mock_input y mock_game_cls no se usan directamente
```

Código DESPUÉS (tests/test_cli.py):

```python
@patch("sys.stdout", new_callable=StringIO)
def test_main_game_exit(self, mock_stdout, _mock_input, _mock_game_cls): #<-- Corregido
    """Prueba el flujo principal y la salida del juego."""
    main()
    # ...
```

**Archivos afectados:** Todos los archivos de tests/

**Estado de la salida:** ✅ Usado sin cambios

**Referencia a archivos finales:**

- core/player.py
- cli/cli.py
- tests/test_game.py
- tests/test_player.py
- core/game.py
- core/dice.py
- tests/* (todos los archivos de tests)

**Resultado final:** Puntuación de Pylint incrementada de ~7.5/10 a **9.57/10**

---
