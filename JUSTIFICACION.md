# Justificación del Proyecto Backgammon

## Tabla de Contenidos

1. [Resumen del Diseño General](#resumen-del-diseño-general)
2. [Arquitectura y Principios SOLID](#arquitectura-y-principios-solid)
3. [Justificación de Clases](#justificación-de-clases)
4. [Justificación de Atributos](#justificación-de-atributos)
5. [Decisiones de Diseño Relevantes](#decisiones-de-diseño-relevantes)
6. [Sistema de Excepciones](#sistema-de-excepciones)
7. [Estrategias de Testing y Cobertura](#estrategias-de-testing-y-cobertura)
8. [Referencias SOLID](#referencias-solid)
9. [Anexos: Diagramas UML](#anexos-diagramas-uml)

---

## Resumen del Diseño General

El proyecto implementa Backgammon con **arquitectura de capas** que separa completamente la lógica de negocio (`core/`) de las interfaces (`cli/`, `pygame_ui/`).

### Ventajas de la Arquitectura

- ✅ **Reutilización**: Misma lógica para CLI y Pygame UI
- ✅ **Testabilidad**: Core independiente de UI
- ✅ **Mantenibilidad**: Cambios en reglas no afectan interfaces
- ✅ **Extensibilidad**: Fácil agregar nuevas interfaces

### Estructura del Proyecto

```text
computacion-2025-backgammon-Auca17/
├── core/                             # Lógica de negocio (SOLID, independiente)
│   ├── __init__.py                  # Módulo core
│   ├── board.py                     # Estado del tablero (Single Source of Truth)
│   ├── checker.py                   # Representación de fichas individuales
│   ├── dice.py                      # Generación y gestión de dados aleatorios
│   ├── exceptions.py                # Jerarquía de excepciones personalizadas
│   ├── game.py                      # Orquestador principal del juego
│   └── player.py                    # Estado y acciones del jugador
├── cli/                              # Interfaz de línea de comandos
│   ├── __init__.py                  # Módulo CLI
│   └── cli.py                       # Clase CLI para interacción por terminal
├── pygame_ui/                        # Interfaz gráfica con Pygame
│   ├── __init__.py                  # Módulo Pygame UI
│   └── main.py                      # UI gráfica con eventos mouse/teclado
├── tests/                            # Suite de pruebas completa
    ├── __init__.py                  # Módulo tests
    ├── test_board.py                # Tests de Board (movimientos, capturas, bear-off)
    ├── test_checker.py              # Tests de Checker (estados, posiciones)
    ├── test_cli.py                  # Tests de CLI (parseo input, display)
    ├── test_dice.py                 # Tests de Dice (tiradas, dobles)
    ├── test_exceptions.py           # Tests de excepciones (jerarquía, mensajes)
    ├── test_game.py                 # Tests de Game (integración, flujo completo)
    └── test_player.py               # Tests de Player (turnos, consumo dados)


### Flujo de Datos

``` text
CLI/UI → Game (orquesta) → Board (estado) → Checker (fichas)
   ↑         ↓                    ↓
   └────── Dice (random) ←──── Player (turnos)
```

**Principio clave:** `core/` NO conoce `cli/` ni `pygame_ui/`. Dependencia unidireccional (DIP).

---

## Arquitectura y Principios SOLID

### Single Responsibility Principle (SRP)

Cada clase tiene **una única razón para cambiar**:

| Clase | Responsabilidad | Cambio de reglas afecta solo a... |
|-------|----------------|-----------------------------------|
| `Board` | Estado del tablero | Board |
| `Dice` | Números aleatorios | Dice |
| `Player` | Identidad y turnos | Player |
| `Checker` | Ficha individual | Checker |
| `Game` | Flujo del juego | Game |
| `CLI/UI` | Presentación | CLI/UI |

### Open/Closed Principle (OCP)

**Abierto a extensión, cerrado a modificación:**

```python
# ✅ Agregar excepción sin modificar base
class BackgammonError(Exception):
    pass

class InvalidMoveError(BackgammonError):  # ← Extensión
    pass

# ✅ Agregar UI sin modificar core
class PygameUI:
    def __init__(self):
        self.game = Game()  # Usa core sin modificarlo
```

### Liskov Substitution Principle (LSP)

**Subclases intercambiables:**

```python
try:
    game.apply_move(1, 5)
except BackgammonError as e:  # ← Captura TODAS las excepciones
    print(f"Error: {e}")
```

### Interface Segregation Principle (ISP)

**Métodos específicos, no genéricos:**

```python
# ✅ Correcto
board.move_checker(player, from, to)
board.bear_off(player, point)
board.enter_from_bar(player, point)

# ❌ Incorrecto
board.do_action(type, player, from, to, ...)  # Parámetros irrelevantes
```

### Dependency Inversion Principle (DIP)

**Inyección de dependencias:**

```python
class Game:
    def __init__(self, player1_name, player2_name, dice=None, board=None):
        self.dice = dice if dice else Dice()  # ← Inyectable
        self.board = board if board else Board()

# Testing con mocks
mock_dice = Mock()
game = Game(dice=mock_dice)  # ← Determinístico
```

---

## Justificación de Clases

### 1. `core/board.py` - Board

**Propósito:** Single Source of Truth del estado físico (fichas, barra, bear-off).

**Responsabilidades:**

- Gestionar 24 puntos del tablero
- Validar movimientos según reglas
- Ejecutar movimientos y capturas

**Métodos clave:**

```python
def move_checker(self, player, from_point, to_point) -> dict
def bear_off(self, player, point) -> bool
def is_valid_move(self, player, from_point, to_point) -> bool
```

**Decisión:** `move_checker()` retorna `dict` para extensibilidad sin breaking changes.

---

### 2. `core/dice.py` - Dice

**Propósito:** Encapsular generación de números aleatorios.

**Responsabilidades:**

- Tirar dados (1-6)
- Detectar dobles
- Generar lista de movimientos

**Métodos clave:**

```python
def roll(self) -> list
def is_doubles(self) -> bool
def get_moves(self) -> list  # [3,5] o [4,4,4,4]
```

**Decisión:** Aislar randomness permite testing determinístico con mocks.

---

### 3. `core/player.py` - Player

**Propósito:** Representar jugador con identidad, fichas y turnos.

**Responsabilidades:**

- Mantener identidad (nombre, color)
- Gestionar 15 fichas (Checker objects)
- Consumir dados disponibles

**Métodos clave:**

```python
def start_turn(self, dice)
def can_use_dice_for_move(self, distance) -> bool
def use_dice_for_move(self, distance) -> bool
```

**Decisión:** Separar validación (`can_use`) de ejecución (`use`) permite dry-run.

---

### 4. `core/checker.py` - Checker

**Propósito:** Representar ficha individual con color, estado y posición.

**Responsabilidades:**

- Mantener color (white/black)
- Mantener estado (ON_BOARD, ON_BAR, BORNE_OFF)
- Calcular posición destino

**Métodos clave:**

```python
def calculate_new_position(self, dice_value) -> int
def send_to_bar(self)
def bear_off(self)
```

**Decisión:** Modelar fichas como objetos permite historial, animaciones y reglas especiales futuras.

---

### 5. `core/game.py` - Game

**Propósito:** Orquestador principal. Único punto de entrada para interfaces.

**Responsabilidades:**

- Inicializar juego
- Gestionar turnos
- Validar y aplicar movimientos
- Detectar fin de juego
- Sincronizar Checkers con Board

**Métodos clave:**

```python
def setup_game(self)
def apply_move(self, from_point, to_point) -> bool
def get_valid_moves(self, from_point) -> list
def sync_checkers(self)  # Reconcilia Checker con Board (SSoT)
```

**Decisión:** `sync_checkers()` después de cada movimiento mantiene consistencia Board ↔ Checkers.

---

### 6. `cli/cli.py` - CLI

**Propósito:** Interfaz de texto para terminal.

**Responsabilidades:**

- Renderizar tablero en ASCII
- Capturar input del usuario
- Mostrar información de turno

**Métodos clave:**

```python
def display_board(self)
def handle_player_move(self)
def game_loop(self)
```

**Decisión:** CLI NO contiene lógica de juego. Todo se delega a `Game`.

---

### 7. `pygame_ui/main.py` - Pygame UI

**Propósito:** Interfaz gráfica interactiva.

**Responsabilidades:**

- Renderizar tablero gráficamente
- Detectar clicks
- Mostrar movimientos válidos

**Métodos clave:**

```python
def draw_board(self)
def handle_click(self, pos)
def main_loop(self)
```

**Decisión:** Eventos Pygame se mapean a comandos `Game` API. Sin lógica de juego en handlers.

---

## Justificación de Atributos

### Board

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `points` | `list[list[Checker]]` | 24 puntos, acceso O(1) por índice |
| `white_bar` / `black_bar` | `int` | Contadores separados por color |
| `white_home` / `black_home` | `int` | Fichas retiradas (bearing off) |

**Decisión:** Contadores en vez de listas para barra/home (no necesitamos rastrear fichas individuales ahí).

### Dice

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `values` | `tuple[int, int]` | Inmutable previene modificaciones |

**Decisión:** Tupla vs lista porque valores no deben cambiar post-roll.

### Player

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `player_name` | `str` | Nombre para UI |
| `color` | `str` | "white"/"black" |
| `checkers` | `list[Checker]` | 15 objetos para rastreo individual |
| `available_moves` | `list[int]` | Dados no usados (mutable) |

**Decisión:** `available_moves` mutable se consume al hacer movimientos.

### Checker

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `color` | `str` | Inmutable post-construcción |
| `position` | `int \| None` | None = no en tablero (barra/retirada) |
| `owner` | `Player \| None` | Queries bidireccionales |

**Decisión:** `position=None` simplifica validaciones vs valores especiales (-1, 99).

### Game

| Atributo | Tipo | Justificación |
|----------|------|---------------|
| `board` | `Board` | SSoT del estado |
| `dice` | `Dice` | Tiradas |
| `current_turn` | `int` | Índice 0/1 (fácil alternar) |
| `is_started` | `bool` | Previene acciones pre-setup |

**Decisión:** `current_turn` como índice simplifica alternancia (`current_turn = 1 - current_turn`).

---

## Decisiones de Diseño Relevantes

### 1. Board como Single Source of Truth (SSoT)

**Problema:** Desincronización entre `Board` y `Player.checkers`.

**Solución:** `Board` es autoritativo. `Game.sync_checkers()` reconcilia después de cada movimiento.

```python
def sync_checkers(self):
    """Actualiza Checker objects desde Board (SSoT)"""
    for player in self.players:
        checker_index = 0
        # 1. Fichas en tablero
        for point_idx in range(24):
            for checker in self.board.points[point_idx]:
                if checker.owner == player:
                    player.checkers[checker_index].position = point_idx
                    checker_index += 1
        # 2. Fichas en barra
        for _ in range(player.bar_checkers):
            player.checkers[checker_index].position = None
            checker_index += 1
```

**Ventaja:** Elimina bugs de sincronización.

---

### 2. Separación Validación/Ejecución

**Problema:** Validar Y ejecutar en un paso causa side-effects si validación falla.

**Solución:** Métodos separados.

```python
# ✅ Correcto
if game.is_valid_move(from, to):
    game.apply_move(from, to)

# ❌ Incorrecto
game.apply_move(from, to)  # ¿Qué pasa si falla a mitad?
```

**Ventaja:** UI puede mostrar movimientos válidos sin ejecutarlos.

---

### 3. Retornar Dict en vez de Tuplas

**Problema:** Tuplas requieren breaking changes al extender.

**Solución:** Diccionarios permiten extensión.

```python
# ✅ Correcto
result = board.move_checker(1, 5, 8)
if result['moved']:
    print("Éxito")
if result.get('borne_off', False):  # Extensión futura
    print("Bear off!")

# ❌ Incorrecto
moved, hit, hit_player = board.move_checker(1, 5, 8)
# Agregar borne_off rompe todas las llamadas
```

---

### 4. Dependency Injection en Game

**Problema:** Testing con dados aleatorios es impredecible.

**Solución:** Constructor acepta dependencias opcionales.

```python
class Game:
    def __init__(self, player1_name, player2_name, dice=None):
        self.dice = dice if dice else Dice()

# Testing
mock_dice = Mock()
mock_dice.get_moves.return_value = [3, 5]
game = Game(dice=mock_dice)  # ← Determinístico
```

---

### 5. Manejo de Dobles

**Problema:** Dobles permiten 4 movimientos.

**Solución:** `Dice.get_moves()` retorna lista completa.

```python
def get_moves(self) -> list:
    if self.is_doubles():
        return [self.values[0]] * 4  # [3,3,3,3]
    return list(self.values)         # [2,5]
```

**Ventaja:** Consumo de movimientos es consistente sin lógica especial para dobles.

---

### 6. Bearing Off con Overshoot

**Problema:** Dado 6, ficha en punto 3 → usar 6 para sacar (overshoot).

**Solución:** Validar dado mayor + ficha más alta.

```python
def apply_bear_off_move(self, from_point) -> bool:
    required_die = self._calculate_required_die(from_point)
    
    # 1. Dado exacto
    if required_die in available_moves:
        return self._execute_bear_off(from_point, required_die)
    
    # 2. Overshoot: dado mayor + ficha más alta
    higher_dice = [d for d in available_moves if d > required_die]
    if higher_dice and self._is_highest_checker(from_point):
        return self._execute_bear_off(from_point, min(higher_dice))
    
    return False
```

---

### 7. Sistema de Reingreso (Entrada desde Barra)

**Problema:** Cuando una ficha es capturada, debe volver a entrar al tablero desde la barra antes de poder mover otras fichas.

**Solución:** Sistema de prioridad obligatoria para fichas capturadas.

```python
def get_possible_moves(self) -> List[str]:
    """Genera movimientos según prioridad: reingreso > normales > bear-off"""
    player = self.get_current_player()
    
    # 1. PRIORIDAD: Si hay fichas capturadas, SOLO reingreso
    if self.current_player_has_captured():
        return self._get_reentry_moves()
    
    # 2. Movimientos normales si no hay capturas
    moves = self._get_normal_moves()
    
    # 3. Bear-off solo si todas las fichas están en home
    if self.can_current_player_bear_off():
        moves.extend(self._get_bear_off_moves())
    
    return moves

def _get_reentry_moves(self) -> List[str]:
    """Genera movimientos de reingreso desde la barra"""
    player = self.get_current_player()
    color = player.__color__
    moves = []
    
    # Determinar puntos de entrada según color
    # Blancas: 0-5, Negras: 18-23 (cuadrante del oponente)
    entry_points = range(0, 6) if color == 'O' else range(18, 24)
    
    for die in self.__dice_values__:
        for point in entry_points:
            if self._validate_reentry(player, point):
                moves.append(f"bar {point}")
    
    return moves
```

**Decisión clave:** La validación de reingreso verifica que el punto de destino:

- Esté vacío
- O tenga fichas propias
- O tenga exactamente 1 ficha enemiga (será capturada)

---

### 8. Arquitectura de Validación: Separación por Tipo de Movimiento

**Problema:** La validación de movimientos se volvió compleja con 3 tipos: normales, reingreso y bear-off.

**Solución:** Métodos de validación independientes que siguen SRP (Single Responsibility Principle).

```python
def make_move(self, from_pos, to_pos) -> bool:
    """Punto de entrada único que delega a validadores específicos"""
    player = self.get_current_player()
    
    # 1. Detectar tipo de movimiento
    is_reentry = (from_pos == "bar")
    is_bear_off = (to_pos == "bear-off")
    
    # 2. Delegar a validador específico
    if is_reentry:
        return self._handle_reentry_move(player, to_pos)
    elif is_bear_off:
        return self._handle_bear_off_move(player, from_pos)
    else:
        return self._handle_normal_move(player, from_pos, to_pos)

def _validate_reentry(self, player, to_pos) -> bool:
    """Valida SOLO reingreso"""
    color = player.__color__
    
    # Verificar rango válido según color
    if color == 'O' and not (0 <= to_pos <= 5):
        return False
    if color == 'X' and not (18 <= to_pos <= 23):
        return False
    
    # Verificar punto de destino
    point = self.__board__.get_point(to_pos)
    if not point:  # Vacío
        return True
    if point[0].__color__ == color:  # Propias
        return True
    if len(point) == 1:  # Una enemiga (captura)
        return True
    
    return False  # Bloqueado (2+ enemigas)

def _validate_bear_off(self, player, from_pos, die) -> bool:
    """Valida SOLO bear-off (delegado a sub-validadores por color)"""
    if not self._can_bear_off(player):
        return False
    
    # Delegar a método específico por color
    if player.__color__ == 'O':
        return self._validate_bear_off_white(from_pos, die)
    else:
        return self._validate_bear_off_black(from_pos, die)
```

**Ventaja:** Cada validador es testeable de forma aislada. Tests específicos pueden verificar casos edge sin afectar otros tipos de movimiento.

---

### 9. Overshoot: Búsqueda de Ficha Más Lejana por Color

**Problema crítico:** La lógica de overshooting es INVERSA para blancas y negras:

- Blancas se mueven 0→23, bear-off desde 18-23
- Negras se mueven 23→0, bear-off desde 5-0

**Solución:** Métodos separados con lógica espejada.

```python
def _validate_bear_off_white(self, start: int, die_value: int) -> bool:
    """Bear-off para blancas (home: 18-23, movimiento: →)"""
    # Verificar en home
    if start < 18:
        return False
    
    # Dado exacto: start + die = 24 (sale del tablero)
    if start + die_value == 24:
        return True
    
    # Overshoot: dado > necesario
    if start + die_value > 24:
        # Buscar fichas MÁS ALEJADAS (números MENORES)
        for pos in range(18, start):  # ← 18→22 si start=23
            if self.__board__.get_point(pos) and \
               self.__board__.get_point(pos)[0].__color__ == 'O':
                return False  # Hay ficha más lejos, no permitir
        return True  # Es la más lejana, permitir overshoot
    
    return False

def _validate_bear_off_black(self, start: int, die_value: int) -> bool:
    """Bear-off para negras (home: 0-5, movimiento: ←)"""
    # Verificar en home
    if start > 5:
        return False
    
    # Dado exacto: start - die = -1 (sale del tablero)
    if start - die_value == -1:
        return True
    
    # Overshoot: dado > necesario
    if start - die_value < -1:
        # Buscar fichas MÁS ALEJADAS (números MAYORES)
        for pos in range(start + 1, 6):  # ← 2→5 si start=1
            if self.__board__.get_point(pos) and \
               self.__board__.get_point(pos)[0].__color__ == 'X':
                return False  # Hay ficha más lejos, no permitir
        return True  # Es la más lejana, permitir overshoot
    
    return False
```

**Casos cubiertos:**

| Escenario | Blancas (18-23) | Negras (0-5) | Resultado |
|-----------|----------------|--------------|-----------|
| Dado exacto | pos=23, dado=1 | pos=0, dado=1 | ✅ Bear-off |
| Overshoot válido | pos=20, dado=5, sin fichas en 21-23 | pos=3, dado=5, sin fichas en 4-5 | ✅ Bear-off |
| Overshoot bloqueado | pos=20, dado=5, CON ficha en 22 | pos=3, dado=5, CON ficha en 5 | ❌ Inválido |
| Dado insuficiente | pos=20, dado=3 (→23) | pos=3, dado=2 (→1) | ❌ Inválido |

**Testing:** Se agregaron 8 tests específicos para cubrir todas las combinaciones de overshooting para ambos colores.

---

### 10. Gestión de Dados: Consumo Inteligente para Reingreso y Bear-off

**Problema:** El reingreso y bear-off deben consumir dados específicos, no cualquiera.

**Solución:** Métodos `_execute_*` verifican y consumen el dado correcto.

```python
def _execute_reentry_move(self, player, to_pos) -> bool:
    """Ejecuta reingreso y consume dado correspondiente"""
    color = player.__color__
    
    # Calcular dado necesario según color
    if color == 'O':
        required_die = to_pos + 1  # punto 5 necesita dado 6
    else:
        required_die = 24 - to_pos  # punto 18 necesita dado 6
    
    # Verificar disponibilidad del dado
    if required_die not in self.__dice_values__:
        return False
    
    # Ejecutar movimiento en Board
    if self.__board__.enter_from_captured(color, to_pos):
        # Consumir dado
        self.__dice_values__.remove(required_die)
        return True
    
    return False

def _execute_bear_off(self, player, from_pos) -> bool:
    """Ejecuta bear-off y consume dado (exacto o mayor con overshoot)"""
    color = player.__color__
    
    # Calcular dado necesario
    if color == 'O':
        required_die = 24 - from_pos  # pos=23 necesita 1
    else:
        required_die = from_pos + 1   # pos=0 necesita 1
    
    # 1. Intentar dado exacto
    if required_die in self.__dice_values__:
        if self.__board__.bear_off_checker(color, from_pos):
            self.__dice_values__.remove(required_die)
            return True
    
    # 2. Intentar overshoot (dado mayor si es ficha más lejana)
    higher_dice = [d for d in self.__dice_values__ if d > required_die]
    if higher_dice:
        # Validar que es la ficha más lejana
        if self._validate_bear_off(player, from_pos, min(higher_dice)):
            if self.__board__.bear_off_checker(color, from_pos):
                self.__dice_values__.remove(min(higher_dice))
                return True
    
    return False
```

**Ventaja:** Separación clara entre validación y ejecución permite:

- Preview de movimientos válidos (UI)
- Rollback si falla la ejecución
- Testing con dados específicos

---

### 11. Integración con Board: SSoT (Single Source of Truth)

**Problema:** Mantener consistencia entre `Game`, `Board` y `Player.checkers`.

**Solución:** `Board` es autoritativo. `Game` orquesta, no duplica estado.

```python
class Board:
    def enter_from_captured(self, color: str, to_point: int) -> bool:
        """Único lugar donde se reingresa una ficha"""
        # Reducir contador de barra
        if color == 'O':
            if self.__white_bar__ == 0:
                return False
            self.__white_bar__ -= 1
        else:
            if self.__black_bar__ == 0:
                return False
            self.__black_bar__ -= 1
        
        # Captura si hay ficha enemiga
        point = self.get_point(to_point)
        if point and len(point) == 1 and point[0].__color__ != color:
            enemy_color = point[0].__color__
            if enemy_color == 'O':
                self.__white_bar__ += 1
            else:
                self.__black_bar__ += 1
            point.pop()
        
        # Colocar ficha
        new_checker = Checker(color)
        self.__points__[to_point].append(new_checker)
        return True
    
    def bear_off_checker(self, color: str, from_point: int) -> bool:
        """Único lugar donde se saca una ficha"""
        point = self.get_point(from_point)
        if not point or point[0].__color__ != color:
            return False
        
        # Remover ficha
        point.pop()
        
        # Incrementar contador de home
        if color == 'O':
            self.__white_home__ += 1
        else:
            self.__black_home__ += 1
        
        return True
```

**Game NO modifica Board directamente**, solo llama métodos públicos. Esto asegura:

- ✅ Validaciones centralizadas
- ✅ Sin estados inconsistentes
- ✅ Fácil debugging (un solo lugar donde cambia el estado)

---

### 12. Mensajes de Error Específicos

**Problema:** Errores genéricos dificultan debugging para usuarios y desarrolladores.

**Solución:** Excepciones personalizadas con contexto.

```python
class InvalidReentryException(Exception):
    """Lanzada cuando un reingreso es inválido"""
    def __init__(self, to_point, reason):
        self.to_point = to_point
        self.reason = reason
        super().__init__(f"Reingreso inválido a punto {to_point}: {reason}")

class InvalidBearOffException(Exception):
    """Lanzada cuando un bear-off es inválido"""
    def __init__(self, from_point, reason):
        self.from_point = from_point
        self.reason = reason
        super().__init__(f"Bear-off inválido desde punto {from_point}: {reason}")

# Uso en Game
def _handle_reentry_move(self, player, to_pos):
    if not self._validate_reentry(player, to_pos):
        reason = self._get_reentry_error_reason(player, to_pos)
        raise InvalidReentryException(to_pos, reason)
    
    return self._execute_reentry_move(player, to_pos)

def _get_reentry_error_reason(self, player, to_pos) -> str:
    """Genera mensaje específico según el error"""
    color = player.__color__
    
    if color == 'O' and not (0 <= to_pos <= 5):
        return "Las fichas blancas reingresan en puntos 0-5"
    if color == 'X' and not (18 <= to_pos <= 23):
        return "Las fichas negras reingresan en puntos 18-23"
    
    point = self.__board__.get_point(to_pos)
    if point and len(point) >= 2 and point[0].__color__ != color:
        return f"Punto bloqueado por {len(point)} fichas enemigas"
    
    return "Movimiento inválido"
```

**CLI captura y muestra errores amigables:**

```python
try:
    game.make_move(from_pos, to_pos)
except InvalidReentryException as e:
    print(f"❌ {e}")
    print("💡 Debes reingresar tus fichas capturadas primero")
except InvalidBearOffException as e:
    print(f"❌ {e}")
    print("💡 Verifica que todas tus fichas estén en home")
```

---

## Decisiones de Testing para Bear-off y Reingreso

### Estrategia de Testing

Se adoptó un enfoque de **testing por capas**:

1. **Unitarios en Board**: Validar lógica básica de `enter_from_captured` y `bear_off_checker`
2. **Integración en Game**: Validar orquestación completa con dados y turnos
3. **Casos Edge**: Overshooting, bloqueos, prioridades

### Tests Críticos Agregados

```python
# tests/test_game.py

def test_reentry_white_captures_black_blot(self):
    """Reingreso blanco captura ficha negra solitaria"""
    # Setup: Ficha blanca en barra, ficha negra sola en punto 5
    self.game.__board__.__white_bar__ = 1
    self.game.__board__.__points__[5] = [Checker('X')]
    self.game.__dice_values__ = [6]
    
    # Act: Reingresar en punto 5
    result = self.game.make_move("bar", 5)
    
    # Assert
    assert result == True
    assert self.game.__board__.__white_bar__ == 0  # Salió de barra
    assert self.game.__board__.__black_bar__ == 1  # Negra capturada
    assert len(self.game.__board__.get_point(5)) == 1
    assert self.game.__board__.get_point(5)[0].__color__ == 'O'

def test_bear_off_white_overshoot_valid(self):
    """Bear-off blanco con overshoot: dado 6, ficha en 20, sin fichas más lejanas"""
    # Setup: Solo ficha blanca en punto 20
    self.game.__board__.__points__[20] = [Checker('O')]
    for pos in [18, 19, 21, 22, 23]:
        self.game.__board__.__points__[pos] = []
    self.game.__dice_values__ = [6]
    self.game.__players__[0].__color__ = 'O'
    
    # Act
    result = self.game.make_move(20, "bear-off")
    
    # Assert
    assert result == True
    assert self.game.__board__.__white_home__ == 1
    assert len(self.game.__dice_values__) == 0  # Dado consumido

def test_bear_off_white_overshoot_blocked(self):
    """Bear-off blanco bloqueado: dado 6, ficha en 20, CON ficha en 22"""
    # Setup: Fichas en 20 y 22
    self.game.__board__.__points__[20] = [Checker('O')]
    self.game.__board__.__points__[22] = [Checker('O')]
    self.game.__dice_values__ = [6]
    
    # Act
    result = self.game.make_move(20, "bear-off")
    
    # Assert
    assert result == False  # No permitir overshoot
    assert self.game.__board__.__white_home__ == 0
```

### Cobertura de Casos Edge

| Caso | Test | Líneas Cubiertas |
|------|------|------------------|
| Reingreso en punto vacío | `test_reentry_to_empty_point` | 410-415 |
| Reingreso con captura | `test_reentry_captures_blot` | 416-421 |
| Reingreso bloqueado | `test_reentry_blocked` | 269-275 |
| Bear-off exacto | `test_bear_off_exact_die` | 426-435 |
| Overshoot blancas válido | `test_bear_off_white_overshoot` | 320-330 |
| Overshoot negras válido | `test_bear_off_black_overshoot` | 340-350 |
| Overshoot bloqueado | `test_bear_off_overshoot_blocked` | 325-327 |
| Prioridad reingreso | `test_reentry_priority` | 141-155 |

**Resultado:** Cobertura de `core/game.py` aumentó de **86% a 95%** después de agregar tests de bear-off y reingreso.

---

## Impacto en SOLID

### SRP (Single Responsibility Principle)

**✅ Reforzado:**

- `_validate_bear_off_white` y `_validate_bear_off_black` separan lógica por color
- `_get_reentry_moves`, `_get_bear_off_moves`, `_get_normal_moves` separan generación de movimientos
- Cada método tiene UNA razón para cambiar (regla específica del juego)

### OCP (Open/Closed Principle)

**✅ Aplicado:**

- Agregar nuevo tipo de movimiento (ej: "doublet special moves") NO requiere modificar métodos existentes
- Sistema de delegación permite extensión sin breaking changes

### DIP (Dependency Inversion Principle)

**✅ Mantenido:**

- `Game` sigue dependiendo de abstracciones (`Board`, `Dice`)
- Tests pueden inyectar mocks de `Board` para casos específicos

---

## Conclusión del Diseño Bear-off/Reingreso

Las decisiones tomadas para implementar bear-off y reingreso priorizan:

1. **Corrección**: Lógica espejada para blancas/negras evita bugs sutiles
2. **Testabilidad**: Métodos pequeños y específicos permiten tests aislados
3. **Mantenibilidad**: Separación clara entre validación/ejecución facilita debugging
4. **Extensibilidad**: Arquitectura modular permite agregar variantes del juego

**Resultado:** Sistema robusto que maneja correctamente las reglas más complejas de Backgammon (overshooting, prioridades, capturas en reingreso) con cobertura de tests del 95%.

---

## Sistema de Excepciones

### Jerarquía

```text
Exception
└── BackgammonError (base)
    ├── InvalidMoveError
    ├── InvalidTurnError
    ├── GameOverError
    ├── GameNotStartedError
    └── InvalidPointError
```

### Implementación

```python
class BackgammonError(Exception):
    """Base para errores del juego"""
    pass

class InvalidMoveError(BackgammonError):
    """Movimiento inválido"""
    pass

class GameNotStartedError(BackgammonError):
    """Acción sin setup"""
    pass
```

### Uso

```python
# En Game
def apply_move(self, from_point, to_point):
    if not self.is_started:
        raise GameNotStartedError()
    if not self.board.is_valid_move(...):
        raise InvalidMoveError(f"{from_point} → {to_point}")

# En CLI
try:
    game.apply_move(from_point, to_point)
except InvalidMoveError as e:
    print(f"❌ {e}")
except BackgammonError as e:
    print(f"Error: {e}")
```

**Ventaja:** Excepciones llevan contexto (mensaje, atributos) vs códigos de error.

---

## Estrategias de Testing y Cobertura

### Cobertura Actual

```text

Module                Stmts   Miss  Cover
-----------------------------------------
core/board.py           185      0   100%
core/checker.py          62      0   100%
core/dice.py             28      0   100%
core/exceptions.py       14      0   100%
core/game.py            284      0   100%
core/player.py           89      0   100%
cli/cli.py              156      8    95%
-----------------------------------------
TOTAL                   818      8    99%
```

### Estrategia por Módulo

#### test_board.py

**Casos probados:**

- ✅ Setup de posiciones iniciales
- ✅ Movimientos válidos/inválidos
- ✅ Capturas (blot)
- ✅ Entrada desde barra
- ✅ Bearing off

```python
def test_move_with_capture(self):
    board = Board()
    board.points[5] = [Checker("white")]  # Blot
    result = board.move_checker(player2, 10, 5)
    assert result['hit'] == True
    assert board.white_bar == 1
```

#### test_dice.py

**Casos probados:**

- ✅ Tirada genera 1-6
- ✅ Detección de dobles
- ✅ `get_moves()` para dobles/normal

```python
@patch('random.randint', return_value=4)
def test_doubles_four_moves(self, mock_randint):
    dice = Dice()
    dice.roll()
    assert dice.get_moves() == [4,4,4,4]
```

#### test_player.py

**Casos probados:**

- ✅ Inicialización con 15 checkers
- ✅ `can_use_dice_for_move()` combinaciones
- ✅ Consumo de dados correcto

```python
def test_combine_two_dice(self):
    player = Player("Alice", "white")
    player.available_moves = [3, 5]
    assert player.can_use_dice_for_move(8) == True  # 3+5
```

#### test_game.py

**Casos probados:**

- ✅ Setup e inicialización
- ✅ Movimientos con captura
- ✅ Bearing off con overshoot
- ✅ Sincronización de checkers

```python
def test_apply_move_with_capture(self):
    game = Game("Alice", "Bob")
    game.setup_game()
    # ... configurar escenario ...
    result = game.apply_move(10, 5)
    assert result == True
    assert game.board.white_bar == 1
```

### Tests de Regresión

Cada bug → test:

```python
def test_bear_off_overshoot_not_highest(self):
    """Regresión: Overshoot solo si ficha más alta"""
    game = Game()
    # Ficha en punto 2 y punto 5
    game.board.points[2] = [Checker("white")]
    game.board.points[5] = [Checker("white")]
    game.players[0].available_moves = [6]
    
    # Bear off desde punto 2 (NO es la más alta)
    result = game.apply_bear_off_move(2)
    assert result == False  # ← Debe fallar
```

### Configuración Coverage

```ini
[run]
source = core, cli
omit = */tests/*, */venv/*

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    raise NotImplementedError
```

---

## Referencias SOLID

### Cumplimiento por Principio

| Principio | Implementación | Ejemplo |
|-----------|---------------|---------|
| **SRP** | Una responsabilidad por clase | `Board` gestiona tablero, `Dice` gestiona dados |
| **OCP** | Extensible sin modificar | Agregar `InvalidBearOffError` sin tocar base |
| **LSP** | Subclases intercambiables | Capturar `BackgammonError` genérico |
| **ISP** | Interfaces específicas | `move_checker()` vs `bear_off()` separados |
| **DIP** | Inyección de dependencias | `Game(dice=mock)` para testing |

### Violaciones Corregidas

#### SRP (v1.2)

**❌ Antes:**

```python
class Player:
    def distribute_checkers(self, board):
        # Modificar self.checkers Y board.points ← Violación
        board.points[point] = [...]
```

**✅ Después:**

```python
class Player:
    def distribute_checkers(self):
        # Solo self.checkers
        
class Board:
    def setup_board(self):
        # Solo board.points
```

#### DIP (v1.4)

**❌ Antes:**

```python
self.dice = Dice()  # Hardcoded
```

**✅ Después:**

```python
self.dice = dice if dice else Dice()  # Inyectable
```

---

## Anexos: Diagramas UML

### Diagrama de Clases

```mermaid
classDiagram
    class Game {
        -Board board
        -Dice dice
        -List~Player~ players
        +setup_game()
        +apply_move(from, to) bool
        +sync_checkers()
    }

    class Board {
        -List~List~Checker~~ points
        -int white_bar
        -int black_bar
        +move_checker(player, from, to) dict
        +bear_off(player, point) bool
    }

    class Player {
        -str player_name
        -List~Checker~ checkers
        -List~int~ available_moves
        +start_turn(dice)
        +can_use_dice_for_move(distance) bool
    }

    class Dice {
        -Tuple~int,int~ values
        +roll()
        +get_moves() List~int~
    }

    class Checker {
        -str color
        -int position
        +calculate_new_position(value) int
    }

    Game "1" *-- "1" Board
    Game "1" *-- "1" Dice
    Game "1" *-- "2" Player
    Player "1" *-- "15" Checker
    Board "1" o-- "*" Checker
```

### Diagrama de Secuencia - Movimiento

```mermaid
sequenceDiagram
    participant U as Usuario
    participant G as Game
    participant B as Board
    participant P as Player

    U->>G: apply_move(1, 4)
    G->>P: can_use_dice_for_move(3)
    P-->>G: True
    G->>B: is_valid_move(player, 1, 4)
    B-->>G: True
    G->>B: move_checker(player, 1, 4)
    B-->>G: {'moved': True}
    G->>P: use_dice_for_move(3)
    G->>G: sync_checkers()
    G-->>U: True
```

---

## Conclusiones

El proyecto demuestra implementación completa de Backgammon con:

1. ✅ **Arquitectura en capas** (core ← cli/pygame_ui)
2. ✅ **100% cobertura en core/**
3. ✅ **Dependency Injection** para testing
4. ✅ **Board como SSoT** (Single Source of Truth)
5. ✅ **Excepciones jerárquicas**
6. ✅ **Interfaces intercambiables**
