# Changelog

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [1.4.9] – 2025-10-29 → Commit 6266e6c

**Archivo:** tests/test_board.py

### Added (Novedades en 1.4.9)

**Nuevos casos de prueba del tablero**  

- `test_bear_off_checker_valid`: retirada correcta (bear-off) desde casa.
- `test_bear_off_checker_invalid`: `ValueError` al intentar bear-off desde punto vacío.
- `test_enter_from_captured`: reingreso al tablero de una ficha capturada.
- `test_enter_from_captured_to_blocked_point`: bloqueo correcto al reingresar en punto ocupado.

### Changed (Novedades en 1.4.9)

#### Refactor de TestBoard

- Simplificación del encabezado del módulo y docstrings.
- `test_move_checker_and_capture` ahora valida con más precisión:
  - Contador del origen, color del destino y cantidad en barra/capturadas.
- Uso consistente de utilidades del `Board` (`get_point`, `get_point_count`, `get_captured`, `get_home`).

### Removed (Novedades en 1.4.9)

- Import innecesario: `from core.checker import Checker`.

### Notes (Novedades en 1.4.9)

- Este commit sólo toca tests; no hay cambios en lógica de producción.
- Mejora la cobertura y claridad de escenarios críticos: captura, barra y bear-off.

---

## [1.4.8] – 2025-10-29 → Commit f42643d

**Archivos:** .coveragerc, cli/cli.py, core/board.py, pygame_ui/main.py, tests/*

### Added  (Novedades en 1.4.8)

**Cobertura (.coveragerc)** (Novedades en 1.4.8)

- `source = core, cli`
- `omit` ampliado: `*/tests/*`, `*/test_*`, `*/__pycache__/*`, `*/venv/*`, `*/env/*`, `*/.venv/*`
- `exclude_lines`: `pragma: no cover`, `__repr__`, `__str__`, `AssertionError`, `NotImplementedError`, `if __name__ == "__main__":`
- Salida XML: `coverage.xml`
- Docstring técnica en `handle_play_events(...)` con parámetros, retorno y notas de uso (atajo de ESPACIO, cambio automático de turno, validaciones).

### Changed (Novedades en 1.4.8)

**pygame_ui/main.py** (Novedades en 1.4.8)

- Limpieza de estilo y comentarios.
- Reescritura menor: `legal_moves.update(get_legal_moves(...))` tras `clear()` (queda en una sola línea).
- `main_loop()` ahora cierra de forma explícita: `pygame.quit(); sys.exit()`.

**Tests de lógica y UI** (Novedades en 1.4.8)

- Normalización de comillas, eventos simulados y `update(...)` de estados.
- Eliminación de duplicados y líneas en blanco para lecturabilidad.

### Fixed

- Consistencia en creación/aplicación de eventos Pygame dentro de los tests (evita flakiness por pequeñas diferencias de formato).

### Removed (Novedades en 1.4.8)

- Importaciones y líneas en blanco innecesarias en `cli/cli.py`, `core/board.py`, y varios `tests/*`.

### Tests / Infra (Novedades en 1.4.8)

- Config de cobertura afinada para CI más honesto (sin ruido de `tests/`, cachés o entornos virtuales).
- Mantiene suites agregadas en 1.4.7; este commit es principalmente de refactor/limpieza sin cambios funcionales en reglas de juego.

---

## [1.4.7] – 2025-10-31 → Commit cb8fa59

**Archivos:** pygame_ui/main.py, tests/test_logic.py, tests/test_ui.py (+594 / −313)

### Added (Novedades en 1.4.7)

**Suite de lógica pura (tests/test_logic.py):**

- **is_inside_triangle:** puntos dentro / fuera / vértice.
- **get_opponent:** casos W/B.
- **can_bear_off:** casos positivos, con fichas en barra, con fichas fuera de casa, "regla exacta" y escenarios de overshoot (excepción).
- **Bear-off:** prioridad de movimiento normal vs. retiro por overshoot.

**UI / Flujo de juego (tests/test_ui.py):**

- **Menú:** clic en "Jugador vs Jugador" → NAME_INPUT.
- **Validación de nombres** (válidos/ inválidos) + mensaje de error.
- **START_ROLL:** avanzar a PLAY con barra espaciadora.
- **PLAY:** lanzar dados, regla de dobles (cuatro movimientos), selección de punto, movimiento válido/inválido.
- **Condición de victoria** y cambio de turno al agotar movimientos.

### Changed (Novedades en 1.4.7)

**Pantallas "dibujables" en modo test (headless):**

- draw_menu y draw_name_input registran buttons/input_boxes aun con surface=None y retornan temprano sin renderizar.
- draw_initial_roll usa first_roll_data.get("rolled", False) y ajusta banner/título.

**Handlers más robustos:**

- handle_menu_events / handle_name_input_events usan game_data.get("buttons", {}) y game_data.get("input_boxes", {}).
- Ingreso de texto: current_name = ...get(player, ""), límite 10 chars y filtro unicode.isprintable().

**Cálculo de movimientos legales:**

- En handle_start_roll_events y handle_play_events se actualiza legal_moves in-place (clear()+update(...)) para preservar referencias compartidas.

**Chequeo de victoria centralizado:**

- Nueva check_for_win(game_data) y uso desde main_loop.

### Fixed (Novedades en 1.4.7)

- Transiciones de fase seguras cuando aún no existen rects de botones/cajas.
- Mensajes consistentes en errores de movimiento ("Error de dado…", "Movimiento no válido.").
- Limpieza de duplicados de dibujo en menú y en ingreso de nombres.

### Removed (Novedades en 1.4.7)

- Bloques de render duplicados en draw_menu y draw_name_input.

**Tests / Infra** (Novedades en 1.4.7)

- Pygame inicializado en modo headless (NOFRAME) para CI estable.
- Mocks para get_point_from_mouse, roll_dice y detección de zonas (puntos, barra, bear-off).

### ⚠️ Nota de reglas (Backgammon)

En can_bear_off se bloquea el bear-off si hay fichas del rival en el cuadrante de casa. Eso no es estándar: si todas tus fichas están en casa (y ninguna en la barra), podés retirar aunque el rival ocupe puntos de tu home. También lo valida el test test_can_bear_off_oponente_en_casa (espera False).
Sugerencia: quitar esa restricción y ajustar/retirar el test asociado para alinear con la regla oficial.

## [1.4.6]

### Added (Novedades en 1.4.6)

- **Suite de lógica pura** (`tests/test_logic.py`):
  - `is_inside_triangle`: puntos dentro/fuera/vértice.
  - `get_opponent`: casos W/B.
  - `can_bear_off`: casos positivos, con fichas en barra, con fichas fuera de casa, “regla exacta” y escenarios de *overshoot* (excepción).
  - Bear-off: prioridad de movimiento normal vs. retiro por *overshoot*.
- **Chequera de victoria**: nueva `check_for_win(game_data)` centraliza el cambio a `GAME_OVER`.

### Changed (Novedades en 1.4.6)

- **`can_bear_off`**: ahora calcula `opponent` y (temporalmente) bloquea el bear-off si hay fichas del rival en el cuadrante de casa del jugador.
- **Pantallas “dibujables” en modo test**:
  - `draw_menu`, `draw_name_input`, `draw_initial_roll` retornan temprano si `surface is None` (modo pruebas headless).
- **Handlers más robustos**:
  - `handle_menu_events`, `handle_name_input_events` usan `game_data.get(...)` y validan presencia de rects.
  - `handle_start_roll_events` limpia/actualiza `legal_moves` tras decidir el ganador de la tirada inicial.
  - `handle_play_events` normaliza el flujo: tira dados con `SPACE`, actualiza `legal_moves`, consume dado y cambia turno cuando corresponde.

### Improved (Novedades en 1.4.6)

- **Legibilidad y testabilidad**:
  - Early-return consistente para `surface is None`.
  - Limpieza de duplicaciones en `main_loop` (victoria delegada a `check_for_win`).
- **UI tests** (`tests/test_ui.py`):
  - Configura Pygame headless (`NOFRAME`).
  - Mocks para `get_point_from_mouse`, `roll_dice` y detección de puntos/barra/bear-off.
  - Casos nuevos: lanzar con `SPACE`, regla de dobles (cuatro movimientos), fin de turno cambia jugador, victoria dispara `GAME_OVER`.

### Fixed (Novedades en 1.4.6)

- Varias rutas de evento que podían dejar `legal_moves` desincronizado ahora hacen `clear()` + `update()` de forma explícita.
- Validaciones de inputs: no se accede a `buttons`/`input_boxes` si no existen.

### ⚠️ Observación importante de reglas (Backgammon)

Se añadió en `can_bear_off` una restricción para **impedir bear-off si hay fichas del oponente en el home del jugador**. Esa condición **no forma parte de las reglas estándar**: mientras **todas tus fichas estén en tu home** (y ninguna en la barra), **podés retirar** aunque el rival ocupe puntos de tu home.  
Esto también se “congela” en `tests/test_logic.py::test_can_bear_off_oponente_en_casa` (espera `False`). Recomendación:

- **Corregir la lógica** quitando ese `return False` por oponente en home.
- **Ajustar/retirar** el test que valida ese comportamiento no estándar.

**Parche sugerido (mínimo):**

```python
def can_bear_off(player, game_state):
    board = game_state["board"]
    if game_state["bar"][player] > 0:
        return False
    home = range(0, 6) if player == PLAYER_WHITE else range(18, 24)
    checkers_in_home = sum(len(board[i]) for i in home if board[i] and board[i][0] == player)
    return checkers_in_home + game_state["off"][player] == 15

```

---

## [1.4.5] – 2025-10-30

### Added (Novedades en 1.4.5)

- **Sistema de Tests Unitarios para UI y Lógica de Fases** (`tests/test_ui.py`):
  - Cobertura completa de **interacciones del jugador** y **transiciones de estado**.
  - Verifica clics, entradas de texto y pulsaciones de teclas sin necesidad de renderizar.
  - Pruebas incluidas:
    - ✅ Clic en “Jugador vs Jugador” cambia a `NAME_INPUT`.
    - ✅ Nombres válidos avanzan a `START_ROLL`.
    - ✅ Nombres inválidos muestran error sin cambiar de fase.
    - ✅ Pulsar `ESPACIO` en `START_ROLL` inicia la partida (`PLAY`).
    - ✅ Simulación de escritura en inputs actualiza nombres correctamente.
    - ✅ Movimiento válido en `PLAY` actualiza tablero y consume dado.
    - ✅ Movimiento inválido deja el estado intacto.
  - Usa **`unittest` + `mock.patch`** para simular clicks y teclado sin entorno gráfico.
- **Funciones modulares para control de eventos** en `main.py`:
  - `handle_menu_events(event, game_data)`
  - `handle_name_input_events(event, game_data)`
  - `handle_start_roll_events(event, game_data, legal_moves)`
  - `handle_play_events(event, game_data, legal_moves)`
  - Separan la lógica de interacción de `main_loop()`, mejorando testabilidad.

### Changed (Novedades en 1.4.5)

- **REPORTS.md**:
  - Se añade nueva sección de encabezado para automatizar reportes (`# Automated Reports`).
  - Bloques de texto delimitados por ```text para Pylint y Coverage.
- **Funciones de dibujo** (`draw_brick_background`, `draw_decorative_banner`, `draw_menu`, `draw_name_input`):
  - Aceptan `surface=None` → Permite ejecución en modo “test” sin inicializar Pygame Display.
  - Añadidos condicionales para saltar renderizado en modo no gráfico.
- **`main_loop()`**:
  - Simplificada: ahora delega el manejo de eventos a las nuevas funciones `handle_*`.
  - Evita duplicación de código entre fases y centraliza control de estado.

### Improved (Novedades en 1.4.5)

- **Testabilidad general** del código Pygame:
  - Todas las pantallas (`MENU`, `NAME_INPUT`, `START_ROLL`, `PLAY`) pueden simularse sin abrir ventana.
  - Los botones y rectángulos (`buttons`, `input_boxes`) se generan incluso sin superficie de dibujo.
- **Legibilidad**:
  - Limpieza de bloques anidados.
  - Comentarios consistentes con el estilo de documentación del proyecto.
- **Mensajes**:
  - Microcopia coherente entre fases (“Mueve…” vs “Mueven…” corregido).

### Fixed (Novedades en 1.4.5)

- **Prevención de errores en tests automáticos**:
  - Llamadas a funciones de dibujo sin `surface` ya no lanzan excepción.
  - Ciclos de evento validados para no modificar el estado fuera de contexto.

---

## [1.4.4] – 2025-10-29

### Added (Novedades en 1.4.4)

- **`draw_decorative_banner(surface)`**: guirnalda de banderines con cuerda curva, sombras y 15 triángulos; usada en **Menú**, **Entrada de Nombres** e **Tirada Inicial**.
- **Tablero “madera sobre ladrillo”**: el `draw_board(...)` ahora pinta **fondo de ladrillos** y encima un **rectángulo de madera** para el área de juego.
- **Contadores de bear-off** renovados: paneles con radio y **ficha indicadora** por color, numerador centrado.

### Changed (Novedades en 1.4.4)

- **Paleta y constantes**: limpieza y unificación de colores (`COLOR_POINT_A/B`, `COLOR_TEXT_DARK= (0,0,0)`, ladrillo/mortero) y normalización de comentarios.
- **Tipografía**: se mantiene la jerarquía (`font_title`, `font_message`, `font_hud[_bold]`, `font_small[_bold]`) y se aplica en textos de botones, labels y mensajes.
- **Geometría**:
  - Cálculo explícito y multilínea de `GAME_AREA_WIDTH` y `POINT_HEIGHT`.
  - Corrección de comas y listas en `point_positions` (arriba/abajo).
- **Estado del juego**:
  - Claves y literales normalizados a **comillas dobles**; `PLAYER_WHITE="W"`, `PLAYER_BLACK="B"`.
  - `setup_initial_state()` devuelve `game_state` coherente y legible (orden y comentarios).
- **Lógica**:
  - `can_bear_off(...)` más claro y robusto.
  - `get_legal_moves(...)`: reingreso desde BAR, movimientos normales y **bear-off con regla de excedente** reescritos; uso de `set(dice)` para evitar duplicados; early-return si hay fichas en barra.
  - `apply_move(...)`: mensajes y envío a barra del oponente formateados; estilo consistente.
- **Render**:
  - `draw_board(...)` reordena el dibujo (ladrillo → madera → triángulos), invierte colores en cuadrantes 1-6/13-18 para mejor patrón, números centrados con `padding` ajustado.
  - `draw_checker(...)` con bordes definidos (gris claro/oscuro).
  - `draw_checkers(...)` muestra **contador xN** a partir de la 6.ª ficha; apila con radio escalado.
  - `draw_highlights(...)` resalta BAR, destinos y área de **OFF**.
- **UI/UX**:
  - **Menú** y **Name Input**: posiciones Y ajustadas (por banner), botones blancos con borde negro y tipografía en negrita.
  - **Mensajes**: barra central translúcida; textos de HUD alineados a derecha/izquierda con ancho máximo para dobles.
  - **Tirada inicial**: paneles desplazados, banner activo y textos oscuros; mensajes “Gana la tirada…” y “Presiona ESPACIO…” reubicados.

### Improved (Novedades en 1.4.4)

- **Legibilidad del código**: formateo PEP-8 (líneas partidas, dicts, comas finales), eliminación de duplicaciones y comentarios aclaratorios.
- **Consistencia** entre fases (`MENU`, `NAME_INPUT`, `START_ROLL`, `PLAY`, `GAME_OVER`) y manejo de eventos/teclas.
- **Detección de clics**: `get_point_from_mouse(...)` devuelve `"BAR"`/`"OFF"`/índice; `is_inside_triangle(...)` con fórmula baricéntrica más explícita.

### Fixed (Novedades en 1.4.4)

- Inconsistencias de color en puntos superiores/inferiores.
- Comas faltantes en tuplas/lists de `point_positions` y parámetros de rectángulos.
- Mensajes y cambios de turno al consumir dado en **bear-off excedente**.

---

## [1.4.3] – 2025-10-29

### Added (Novedades en 1.4.3)

- **Nueva paleta “brick”** para fondos: `COLOR_BRICK` (ladrillo) y `COLOR_MORTAR` (junta).
- **Fuentes en negrita adicionales**: `font_hud_bold` (24, bold) y `font_small_bold` (16, bold).
- **`draw_brick_background(surface)`**: generador de **fondo de pared de ladrillos** (patrón con offset por fila y radios redondeados).

### Changed (Novedades en 1.4.3)

- **Contraste de texto**: `COLOR_TEXT_DARK` pasa a **(0, 0, 0)** (negro) para máximo contraste.
- **Menú / Inputs / Tirada inicial** ahora **dibujan el fondo de ladrillos** con `draw_brick_background(...)`.
- **Botonería**:
  - Botón principal “Jugador vs Jugador” y “Comenzar Partida” ahora con **fondo blanco** y **borde negro**; texto en `font_hud_bold`.
- **Pantalla de nombres**:
  - Labels “Jugador 1/2 …” en **negrita** (`font_hud_bold`).
  - Texto dentro de inputs en **negrita** (`font_hud_bold`).
  - Leyenda de caracteres con `font_small_bold` y color oscuro.
  - Mensaje de error renderizado con **`font_message`** (mejor jerarquía visual).
- **Tirada inicial**:
  - Mensaje “Gana la tirada: …” ahora en **COLOR_TEXT_DARK**.
  - Indicador “Presiona ESPACIO…” en **negrita oscura** (`font_hud_bold`).
- **Microcopia**: mensaje al empezar el juego cambia de **“Mueven …”** a **“Mueve …”**.

### Improved (Novedades en 1.4.3)

- **Accesibilidad y legibilidad**: mayor contraste en textos y botones, jerarquía tipográfica clara.
- **Consistencia visual** entre pantallas con un **tema medieval de ladrillos** cohesivo.
- **Mantenibilidad**: unificación de estilos mediante nuevas constantes y fuentes bold.

---

## [1.4.2] – 2025-10-29

### Added (Novedades en 1.4.2)

- **Tema de UI para pantallas de menú**: constantes nuevas de color  
  `COLOR_MENU_BG`, `COLOR_BUTTON_PRIMARY`, `COLOR_TEXT_DARK`.
- **Fuentes nuevas**: `font_title` (48, bold) para títulos y `font_small` (16) para ayudas/leyendas.
- **`draw_dice(value, x, y, size=50)`**: dado gráfico **escalable** con `size` y puntos posicionados proporcionalmente.
- **Texto guía de longitud** en la pantalla de nombres: “Mínimo 2, máximo 10 caracteres.”

### Changed (Novedades en 1.4.2)

- **Menú principal**: rediseño moderno/minimalista sobre `COLOR_MENU_BG`, título con `font_title` y **botón redondeado** “Jugador vs Jugador” usando `COLOR_BUTTON_PRIMARY`.
- **Pantalla de entrada de nombres**:
  - Se agrega **panel central**; **inputs redondeados** con borde que cambia según el campo activo.
  - Botón **“Comenzar Partida”** con estilo consistente al menú.
  - Mensajes de error reubicados con mejor contraste.
- **Tirada inicial**:
  - Título “**Tirada Inicial**” con `font_title`.
  - Paneles izquierdo/derecho para cada jugador y **dados grandes** (función nueva escalable).
  - Mensajes “**Gana la tirada: …**” y “**Presiona ESPACIO para comenzar**” con jerarquía visual.
- **Tipografía del tablero**: `font_point_num` ahora **18 px en negrita** para mejorar legibilidad de numeración.

### Improved (Novedades en 1.4.2)

- **Consistencia visual** entre menú, formulario de nombres y tirada inicial (paleta, tipografías, radios y márgenes).
- **Legibilidad y contraste** en labels, botones y mensajes (uso de `COLOR_TEXT_DARK` y `COLOR_BUTTON_PRIMARY`).
- **Mantenibilidad**: se **reemplaza** la versión anterior de `draw_dice()` por la versión única y escalable.

---

## [1.4.1] - 2025-10-29

### Changed (Novedades en 1.4.1)

- **Refactor de layout y HUD en Pygame** (`pygame_ui/main.py`, +206 −112, commit `4e2cfee`):
  - Resolución por defecto: **1024×768** (antes 1000×700).
  - Tipografía de numeración de puntos: **18 px bold** (mejor legibilidad).
  - Geometría nueva y explícita:
    - `HUD_TOP_MARGIN`, `HUD_HEIGHT`, `BOARD_MARGIN_X/Y`, `BOARD_TOP_Y`, `BOARD_BOTTOM_Y`, `BOARD_PLAY_HEIGHT`.
    - `BEAR_OFF_WIDTH` y `BOARD_BEAR_OFF_GAP` para separar tablero y columna de **bear-off**.
    - `BAR_WIDTH` ahora **70**; recálculo de `POINT_WIDTH` y `POINT_HEIGHT`.
  - Recomputo de **`point_positions`** con los márgenes nuevos; números centrados en la “calle” media.
  - **HUD superior** renovado (turno a la izquierda; **dados** y **movimientos** alineados a la derecha).
  - **Barra de mensajes** centrada sobre el tablero (overlay translúcido).

### Added (Novedades en 1.4.1)

- **`draw_checker()`**: fichas con borde (look más limpio).
- **`draw_dice()`** y **mejor UI de tirada inicial**: muestra dados gráficos junto a los nombres.
- **Paneles de bear-off** a la derecha (arriba Negras / abajo Blancas) con contador grande y ficha indicadora.
- **`is_inside_triangle()`** para detección precisa de clic en triángulos.

### Improved (Novedades en 1.4.1)

- Radio de ficha en puntos: `0.38 * POINT_WIDTH`; stack con contador desde la **6.ª** ficha.
- Posiciones de fichas en **barra** y **bear-off** ajustadas al nuevo layout.
- **Resaltados**: barra y zona de bear-off usan rectángulos adecuados al rediseño.
- Validación de nombres: ahora exige **2–10** caracteres y muestra mensaje de error en la pantalla de entrada.

---

## [1.4.0] - 2025-10-29

### Added (Novedades en 1.4.0)

- **Menú principal y flujo de inicio** en `pygame_ui/main.py`:
  - **Fase `MENU`** con botón **“Jugador vs Jugador”**.
  - **Fase `NAME_INPUT`** con campos de texto para **nombres de Jugador 1 (Blancas)** y **Jugador 2 (Negras)**, validación mínima (≥ 2 caracteres) y botón **“Comenzar Partida”**.
  - **Fase `START_ROLL`** con pantalla dedicada a la **tirada inicial** (muestra nombres y valores; resuelve empates; **ESPACIO** para iniciar).
  - **HUD** muestra **nombre y color** del jugador en turno.
  - Detección de clic en **zona de bear-off** (`'OFF'`) además de **barra** (`'BAR'`) y puntos.
  - Estructuras UI añadidas al estado: `player_names`, `active_input`, `input_boxes`, `buttons`.

### Changed (Novedades en 1.4.0)

- **Máquina de estados del juego**: `game_phase` amplía fases → `MENU`, `NAME_INPUT`, `START_ROLL`, `PLAY`, `GAME_OVER`.
- **Entrada de usuario**:
  - Manejo unificado por fase en `main_loop()` y nueva función **`handle_play_events`** para la fase de juego.
  - `get_point_from_mouse()` ahora puede devolver `'OFF'` y mejora la detección de áreas.
- Mensajería del HUD y pantallas dedicadas: `draw_menu`, `draw_name_input`, `draw_initial_roll`.

### Notes (Novedades en 1.4.0)

- Ejecutar: `python pygame_ui/main.py`. Requisito: `pygame`.
- No hay cambios en APIs de `core/` ni en el **CLI**.

**Commit relacionado:** `9a6cdbe` — *Add main menu and name input functionality to Backgammon game*.

---

## [1.3.0] - 2025-10-29

### Added (Novedades en 1.3.0)

- **Nueva aplicación gráfica con Pygame**:
  - **Tablero 2D completo** con puntos 1–24, barra central, zona de salida (bear-off) y contador cuando un punto tiene >5 fichas.
  - **HUD informativo**: turno, valores de dados, movimientos disponibles y mensajes de estado.
  - **Resaltados interactivos** del punto de origen y **todos los destinos legales**.
  - **Entrada de usuario**:
    - Clic para **seleccionar origen/destino**.
    - **Barra espaciadora** para tirar los dados (dobles → 4 movimientos).
    - **R** para **reiniciar** la partida.
    - Cierre de ventana para salir.
  - **Lógica de juego integrada** en la UI:
    - Tirada inicial para decidir quién empieza (resuelve empates).
    - Cálculo de **movimientos legales** (normales, reingresos desde **BAR**, y **bear-off** con regla exacta y de **excedente**).
    - **Capturas** (blots) y envío a barra del oponente.
    - **Consumo de dados** por movimiento y **cambio de turno** automático.
    - **Detección de victoria** (15 fichas fuera).
  - **Modelo de estado único** (`game_state`) con: `board`, `bar`, `off`, `current_player`, `dice`, `moves_remaining`, `selected_point`, `message`, `game_phase`, `first_roll_data`.

### Changed (Novedades en 1.3.0)

- No se modifican APIs de `core/` ni el **CLI**; esta versión **añade** una app alternativa con interfaz gráfica.

### Notes (Novedades en 1.3.0)

- **Dependencia nueva:** `pygame` (>= 2.0). Instalar: `pip install pygame`.
- **Ejecución:** `python -m pygame_ui.main`  o  `python pygame_ui/main.py`.
- **Compatibilidad:** sin cambios en pruebas existentes.

**Commit relacionado:** `c27e6d0` — *Implement complete Backgammon game logic and UI using Pygame*.

---

## [1.2.3] - 2025-10-29

### Fixed (Correcciones en 1.2.3)

- **`core/game.py`**
  - `reset()` ahora reinicia el juego **preservando dependencias**: invoca el constructor con `players`, `board` y `dice` para evitar estados nulos o inconsistentes.
  - `make_move()` ajustado para **no devolver booleanos**; ejecuta la acción y deja el estado consistente (consumo de dados, turnos, victoria). Los tests se actualizaron en consecuencia.

### Added (Cambios en 1.2.3)

- **Pruebas unitarias ampliadas y de integración (`tests/`):**
  - **`tests/test_board.py`**
    - `test_get_point()` verifica contenido de un punto en estado inicial.
    - `test_get_2d_representation_with_captured_checkers()` valida que la barra muestre correctamente `W:1 B:1` tras capturas simétricas.
  - **`tests/test_exceptions.py`**
    - Estructura base con `setUp()` para escenarios de errores y excepciones en `Game/Board`.
  - **`tests/test_game.py`**
    - Ajustes por nueva semántica de `make_move()` (se invoca sin `assertTrue`).
    - Casos nuevos:
      - Reingreso **jugador negro** y consumo de dado.
      - **Bear off** jugador negro y consumo de dado.
      - Validación de **bear off** con dado incorrecto (lanza `ValueError`).
      - Llamada a `display_board()` (cobertura).
      - Validación de reingreso negro con dado inválido.
      - Intento de mover ficha del **oponente** (lanza `ValueError`).
      - Reingreso bloqueado (sin movimientos posibles).
      - Movimiento normal negro y consumo de dado.
      - **Reset del juego** deja el estado inicial (jugador actual y dados).
      - Fallo de bear off y de movimiento normal (excepciones).
      - `get_winner()` sin ganador devuelve `None`.
  - **`tests/test_player.py`**
    - Gestión de lista de fichas del jugador:
      - `add_checker`, `remove_checker` (existente y no existente) con verificaciones de integridad.

### Changed (Ajustes en 1.2.3)

- **Homogeneización de docstrings** en módulos de test (`"""Este módulo..."""`) y mensajes de precondición/resultado esperado.
- Limpieza de asertos que dependían del retorno de `make_move()`; ahora se valida por **efectos en estado** (consumo de dados, posiciones, turnos).

---

## [1.2.2] - 2025-10-29

### Added (Cambios en 1.2.2)

- **Nuevas pruebas unitarias ampliadas (`tests/`):**
  - **`test_checker.py`** — agregado nuevo módulo de pruebas para la clase `Checker`:
    - Verifica la inicialización correcta con colores válidos e inválidos.
    - Comprueba el método `move_to()` asegurando actualización de posición.
    - Testea el método `capture()` y su efecto sobre el estado y posición (`bar`).
    - Incluye validación del método `__repr__` con formato `Checker(color)`.
  - **`test_board.py`** — se amplía cobertura de la clase `Board` con pruebas de errores y escenarios reales:
    - Movimiento desde punto vacío o color incorrecto lanza `ValueError`.
    - Movimientos fuera del tablero lanzan `IndexError`.
    - Verificación de capturas y correcto almacenamiento en la barra.
    - Validación de “bear off” correcto e intento inválido desde punto vacío.
    - Reingreso de fichas desde la barra (`enter_from_captured`) y bloqueo de puntos ocupados.
  - **`test_game.py`** — nuevos casos agregados para la lógica del juego:
    - Verifica comportamiento de tiradas dobles (`roll_dice`) → genera cuatro movimientos.
    - Comprueba condiciones de “bear off” válidas e inválidas.
    - Valida detección del final de partida y asignación del ganador (`is_over()` y `get_winner()`).
    - Prueba movimientos posibles desde la barra y durante el “bear off”.
    - Añade validación de `_validate_move()` frente a dados no coincidentes.
  - **`test_player.py`** — refactor completo y expansión de cobertura:
    - Validación de inicialización de jugador con nombre y color correctos.
    - Nuevas pruebas para gestión de fichas en la barra (`add_bar_checker`, `remove_bar_checker`).
    - Añadidas verificaciones de seguridad ante barras vacías.
    - Contadores de fichas “en casa” (`add_home_checker`, `get_home_checkers`) correctamente actualizados.

### Changed (Cambios en 1.2.2)

- **Refactor menor en `test_player.py`:**
  - Se reemplazaron funciones heredadas de `setUp` por métodos individuales de inicialización por prueba.
  - Aclaración de docstrings, uniformando el formato de precondiciones y resultados esperados.
  - Actualización de nomenclatura de métodos de test para mayor coherencia con el estándar `unittest` (prefijo `test_` en todos los casos).

- **Cobertura de código general:**
  - Cobertura extendida a los módulos críticos del núcleo (`core/board`, `core/checker`, `core/game`, `core/player`).
  - Documentación interna (docstrings) alineada con las nuevas pruebas y mensajes de error esperados.
  - Preparación para futura integración de validaciones automáticas en CI/CD.

### Fixed (Correcciones en 1.2.2)

- **Revisión de mensajes de error en el módulo `Board`:**
  - Se corrigen valores esperados en excepciones (`ValueError`, `IndexError`) dentro de los tests para asegurar coincidencia exacta con el comportamiento del código fuente.
  - Validación correcta de reingreso de fichas desde la barra cuando no hay fichas capturadas.

- **Coherencia entre módulos de prueba:**
  - El flujo de inicialización y teardown es ahora consistente entre `test_board.py`, `test_player.py` y `test_game.py`.
  - Eliminación de redundancias en verificaciones de color y puntos de tablero.

---

## [1.2.1] - 2025-10-26

### Added (Cambios en 1.2.1)

- **Mejoras interactivas en el CLI (`cli/cli.py`):**
  - Se agregó una nueva función `_get_player_names()` que solicita los nombres de ambos jugadores con validación de entrada.
  - Implementada `_decide_first_player()`:
    - Realiza una tirada inicial de dados (1–6) para determinar quién comienza.
    - Muestra los resultados en pantalla y gestiona empates con repeticiones automáticas.
    - Devuelve el índice del jugador que inicia la partida.
  - Nuevo método `_display_possible_moves()` que imprime las jugadas válidas **en formato vertical**, una por línea, mejorando la legibilidad durante la ejecución del CLI.
  - Integración con la función principal `main()`:
    - Flujo mejorado paso a paso:
      1. Solicita nombres.
      2. Decide quién comienza mediante tirada aleatoria.
      3. Inicializa instancias de `Board`, `Dice` y `Player`.
      4. Lanza el juego con `Game(player1, player2, board, dice)`.

- **Refactorización de flujo de inicio (`core/game.py`):**
  - Simplificación de `start()` para delegar la tirada inicial de dados a un nuevo método `roll_dice()`.
  - Documentación revisada y comentarios más claros.

### Changed (Cambios en 1.2.1)

- **Interfaz de línea de comandos (CLI):**
  - Se eliminó la tirada automática inicial de `Game.start()` dentro del núcleo, trasladándola al CLI para una interacción más natural con el usuario.
  - Estructura del flujo de inicio reorganizada en bloques comentados (`#1`, `#2`, `#3`, `#4`) para mayor claridad del código.
  - Salida en consola completamente traducida al español, incluyendo mensajes de empate y reinicio de tirada.
  - Remplazo del mensaje horizontal de movimientos (`', '.join(moves)`) por la impresión vertical mediante `_display_possible_moves()`.

- **Excepciones (`core/exceptions.py`):**
  - Limpieza de clases base (`BackgammonException`, `InvalidMoveException`, `OutOfBoundsException`, `InsufficientDiceException`, `NoPiecesException`).
  - Eliminación de sentencias redundantes `pass`, conservando solo la definición con docstring.
  - Código más limpio, coherente con las normas **PEP 8** y **Black**.

### Fixed (Correcciones en 1.2.1)

- **Tests actualizados (`tests/test_game.py`):**
  - Ajuste de nombres de funciones de test:
    - `test_start_game_sets_turn_and_dice()` → `test_start_rolls_dice()`.
  - Actualización de asserts para reflejar el nuevo comportamiento:
    - Validación de que los dados se lanzan correctamente en la primera tirada.
    - Verificación de que se asigna el jugador inicial basado en la tirada.
  - Limpieza de comentarios y mayor coherencia de lenguaje (español técnico).

- **Integración CLI–Core revisada:**
  - Se asegura que la partida arranque con el jugador correspondiente tras la tirada inicial.
  - Corrección de pequeños problemas de formato y espaciado durante la impresión del tablero y los mensajes.

---

## [1.2.0] - 2025-10-25

### Added (Cambios en 1.2.0)

- **Refactorización SOLID del núcleo del juego (`core/`):**
  - `Game` ahora utiliza **inyección de dependencias explícita** para `Board` y `Dice`, asegurando independencia entre módulos y mayor facilidad de prueba.
  - Se reorganizaron los métodos principales en submétodos privados:
    - `_get_reentry_moves()`, `_get_bear_off_moves()` y `_get_normal_moves()` para calcular jugadas posibles.
    - `_execute_bear_off()` y `_execute_normal_move()` para realizar movimientos validados.
  - Implementación más limpia y legible, acorde al principio de **Responsabilidad Única (SRP)**.

- **Actualización del CLI (`cli/cli.py`):**
  - Nuevo flujo de ejecución estructurado con bienvenida, instrucciones y salida controlada con `"salir"`.
  - Impresión formateada del turno, tirada de dados y estado del tablero.
  - Separadores visuales y mensajes traducidos completamente al español.
  - Integración directa con las nuevas dependencias del núcleo (`Board`, `Dice`, `Game`).

- **Reescritura de validaciones en `core/board.py`:**
  - `move_checker()` y `enter_from_captured()` ahora gestionan correctamente fichas capturadas.
  - Fichas enemigas únicas en un punto se capturan automáticamente y se almacenan en `__captured__`.
  - Estandarización de comillas, formato y docstrings.
  - Mejora de salida textual en el tablero (`display_board()`), con:
    - Contadores centrados para barra y casa.
    - Fichas representadas con `"O"` (blancas) y `"X"` (negras).
    - Texto unificado de resumen al final del tablero.

- **Actualización de `core/dice.py`:**
  - Se inicializan los atributos `__value1__` y `__value2__` con valores nulos.
  - Mejora de documentación interna y consistencia de estilo (Black).

- **Expansión y mejora de pruebas unitarias (`tests/`):**
  - `tests/test_game.py`:
    - Alineado con la nueva firma del constructor de `Game`.
    - Se agregan tests para movimientos válidos, reingresos, “bear off”, bloqueo de puntos y condiciones de victoria.
    - Control explícito de turno y valores de dado.
  - `tests/test_exceptions.py`:
    - Nueva configuración del entorno de pruebas con `Board` y `Dice` inyectados.
  - `tests/test_board.py`:
    - Limpieza de asserts redundantes y uniformización de estilo.
  - `tests/test_dice.py`:
    - Ajuste en `unittest.mock.patch` para soportar decoradores `@patch("core.dice.Dice.roll")`.

### Changed (Cambios en 1.2.0)

- **Constructor del juego:**
  - Viejo: `Game(__player1__=None, __player2__=None)`
  - Nuevo: `Game(player1, player2, board, dice)`
  - Permite mayor control desde CLI y tests sin crear dependencias internas.
- **Estructura interna de `Game`:**
  - `get_possible_moves()` delega la lógica en funciones separadas según el estado (reingreso, “bear off”, normal).
  - Validaciones `_validate_move`, `_validate_bear_off` y `_validate_reentry` completamente reescritas.
- **Código estandarizado con Black y principios SOLID:**
  - Corrección de sangrías, comillas dobles, docstrings coherentes y separación de responsabilidades por módulo.
- **CLI optimizado:**
  - Doble impresión de líneas eliminada.
  - Mensajes redundantes reemplazados por una versión clara y resumida.

### Fixed (Correcciones en 1.2.0)

- **Capturas de fichas corregidas:**
  - Evita errores al intentar mover a puntos bloqueados con más de una ficha enemiga.
- **Consumo de valores de dado:**
  - Los movimientos válidos eliminan correctamente el valor correspondiente en `__dice_values__`.
- **Turnos automáticos:**
  - El turno cambia solo si no quedan dados disponibles y la partida sigue activa.
- **Validaciones reforzadas:**
  - Se verifican distancias y cuadrantes válidos para movimientos de “bear off”.
  - Se corrigen mensajes de error para reflejar la causa exacta de los fallos.

### Tests (Cambios en 1.2.0)

- **Compatibilidad con nuevo diseño:**
  - Todos los tests usan la nueva firma `Game(player1, player2, board, dice)`.
  - Se eliminaron dependencias de inicialización implícita.
- **Mayor legibilidad y mantenimiento:**
  - Comentarios aclaratorios añadidos sobre las razones de cada cambio.
  - Secciones de código alineadas con Black.
- **Cobertura funcional extendida:**
  - Casos de prueba para escenarios sin movimientos válidos, captura de fichas, y validaciones de “bear off”.

---

## [1.1.0] - 2025-10-23

### Added (Cambios en 1.1.0)

- **Representación 2D del tablero de Backgammon:**
  - Nueva función `get_2d_representation()` en `core/board.py` que genera una vista textual del tablero con todos los puntos, fichas visibles, barra de capturas y fichas fuera de casa.
  - Muestra el estado completo en consola incluyendo:
    - Fichas blancas (‘O’) y negras (‘X’).
    - Contadores superiores e inferiores numerados (1–24).
    - Fichas capturadas y fichas “en casa”.
  - Integración con `Game.display_board()` para mostrar automáticamente la versión 2D del tablero durante la ejecución del CLI.

- **Sistema de movimientos posibles dinámicos según tirada de dados:**
  - Nuevo método `get_possible_moves()` en `core/game.py`.
  - Calcula todas las jugadas válidas disponibles para el jugador actual basadas en:
    - Valores obtenidos en los dados.
    - Posiciones de fichas del jugador.
    - Reingresos desde la barra y movimientos de “bear off”.
  - Integra validaciones de reingreso (`validate_reentry`) y extracción (`validate_bear_off`) dentro del flujo principal del juego.
  - Devuelve una lista descriptiva con formato humano (por ejemplo: `["Barra a 5", "6 a 10"]`).

- **Actualización del CLI (`cli/cli.py`):**
  - Muestra el tablero en formato 2D cada turno.
  - Presenta los movimientos posibles en texto antes de que el jugador ingrese su jugada.
  - Incluye control automático de turnos cuando no hay movimientos válidos disponibles.
  - Traducción completa de los mensajes al español, coherente con la interfaz anterior.

- **Nuevas pruebas unitarias (`tests/`):**
  - `test_board.py`: agrega `test_get_2d_representation()` para verificar que el tablero 2D se genere correctamente y contenga todos los encabezados y barras esperadas.
  - `test_game.py`: agrega `test_get_possible_moves_no_moves()` para validar el comportamiento cuando un jugador no tiene jugadas disponibles.
  - Validaciones adicionales sobre `make_move()` y `get_possible_moves()` para asegurar coherencia entre jugadas, tiradas y estados del tablero.

### Changed (Novedades en 1.1.0)

- `Game.display_board()` ahora imprime directamente la representación generada por `Board.get_2d_representation()`.
- `Board.move_checker()` optimizado para manejo de errores y extracción controlada de fichas.
- `cli.main()` reorganizado:
  - Agregada gestión de listas de movimientos posibles antes de la solicitud de entrada.
  - Eliminadas comprobaciones redundantes de `get_dice_values()` en favor de `get_possible_moves()`.
- Estructura de los mensajes del CLI reformulada para mayor claridad en la interacción con el jugador.

### Fixed (Novedades en 1.1.0)

- Solucionado un bug en la lógica de cambio de turno cuando un jugador no tiene movimientos válidos.
- Corrección de la impresión de dados en CLI, que ahora refleja exactamente el estado interno de `Game`.
- Ajustes menores en la función `move_checker()` para evitar errores al intentar mover desde un punto vacío.
- Corregida la validación de “puntos bloqueados” que arrojaba `ValueError` de forma prematura.
- Se estandarizó la indentación y formato del código según la guía de estilo Black.

---

## [1.0.0] - 2025-10-22

### Added (Cambios en 1.0.0)

- **Implementación completa del CLI** para Backgammon:
  - Nuevo archivo `cli/cli.py` con interfaz de línea de comandos funcional.
  - Permite iniciar partidas, lanzar dados, mover fichas, mostrar el tablero y finalizar el juego.
  - Mensajes y docstrings traducidos completamente al español.
  - Control de flujo de turnos, detección de finalización y visualización dinámica del estado del tablero.
- **Reestructuración y ampliación del núcleo (`core/`):**
  - `Game`: control total del flujo del juego, inicio de partida, cambio de turno, lanzamiento de dados, validación de movimientos y detección del ganador.
  - `Board`: administración de los puntos, fichas capturadas y posiciones iniciales estándar; manejo de errores con excepciones descriptivas.
  - `Checker`: representación de cada ficha, con su color, posición y estado de captura.
  - `Player`: ampliado con atributos para fichas en barra y en casa; nuevos métodos para añadir, eliminar y contar fichas.
  - `Dice`: encapsulación del comportamiento de los dados y sus valores; integración con `unittest.mock` para testeo.
- **Sistema completo de pruebas unitarias (`tests/`):**
  - `test_board.py`: verificación de inicialización del tablero y movimiento de fichas.
  - `test_dice.py`: validación de los valores de los dados, comportamiento con `mock` y detección de dobles.
  - `test_game.py`: pruebas de flujo general del juego, cambios de turno, validaciones de movimiento, condiciones de victoria y reingresos.
  - `test_player.py`: validación de inicialización de jugadores y manipulación de fichas en la lista, barra y casa.
  - `test_exceptions.py`: cobertura de excepciones (`IndexError`, `ValueError`) en movimientos inválidos.
- **Documentación interna (docstrings) unificada y en español**:
  - Cada clase y método ahora posee descripción, argumentos y retorno claramente definidos.
  - Estandarización de estilo y prefijos privados (`__atributo__`).
- **Compatibilidad total entre módulos y pruebas.**
  - Todos los componentes (`core/`, `cli/`, `tests/`) funcionan integradamente.
  - Se establece la base para futuras extensiones del juego (interfaz gráfica, red, etc.).

### Fixed (Cambios en 1.0.0)

- Corrección de inconsistencias de nombres entre atributos y métodos (`_color__`, `from_pos`, `to_pos`, `_player__`, etc.).
- Solución de errores en la inicialización del juego:
  - Los jugadores ahora se crean correctamente por defecto si no se especifican instancias.
  - El turno inicial y los dados se determinan correctamente al comenzar la partida.
- Arreglo de validaciones de movimiento:
  - Control de puntos fuera del rango (0–23) mediante `IndexError`.
  - Captura correcta de fichas rivales únicas y actualización de las listas de fichas capturadas.
  - Validaciones completas para reingreso desde la barra (`enter_from_captured`) y extracción (`bear_off`).
- Corrección de errores en la clase `Player`:
  - Inicialización correcta de contadores de fichas en barra y casa.
  - Métodos `add_checker`, `remove_checker`, `add_bar_checker`, `remove_bar_checker` actualizados para mantener coherencia interna.
- Ajuste del método `display_board()` en `Game` para mostrar el tablero de manera legible en CLI.
- Traducción y corrección de todos los tests:
  - Nombres de variables, asserts y docstrings adaptados al nuevo formato en español.
  - Uso correcto de `mock.patch` para simular tiradas de dados.
- Eliminación de imports relativos erróneos y normalización del árbol de dependencias internas.

---

## [0.9.1] - 2025-10-06

### Added (Cambios en 0.9.1)

- Se incorporaron pequeñas mejoras internas en la inicialización y control de flujo de las clases del core:
  - **`Board`**: refactor del método `move_checker` con validaciones más seguras para fichas capturadas, límites del tablero y puntos bloqueados.
  - **`Player`**: ahora incluye contadores de fichas en barra (`bar_checkers`) y en casa (`home_checkers`) para un seguimiento más preciso del estado.
  - **`Game`**: se simplificó la gestión de turnos con `current_turn` y `switch_turn`, y se agregaron comprobaciones de jugador actual.
  - **`Checker`**: ahora garantiza valores válidos de color (`white` o `black`) y mejora el manejo de fichas capturadas.
  - **`Dice`**: limpieza del método `is_double()` y unificación del formato de retorno.
- Se extendieron los **tests unitarios** para cubrir los nuevos comportamientos:
  - `test_board.py`: validación de movimientos y actualización de conteos.
  - `test_dice.py`: se agregaron mocks sobre `random.randint` y test de dobles.
  - `test_exceptions.py`: pruebas de excepciones personalizadas de Backgammon.
  - `test_game.py` y `test_player.py`: ampliadas pruebas de cambio de turno y manipulación de fichas.

---

### Changed (Cambios en 0.9.1)

- Se aplicó **formateo Black** a todo el proyecto (`cli/`, `core/` y `tests/`), estandarizando:
  - indentación a 4 espacios,
  - saltos de línea consistentes,
  - uso uniforme de comillas dobles.
- Ajustes en nombres internos y simplificación de bloques `if` anidados.
- Se mejoró la legibilidad general del código y se redujo la redundancia en varios métodos de las clases principales.
- Actualizados los comentarios y docstrings para mayor coherencia con la estructura actual.
- Se corrigió el flujo de importaciones relativas para mantener consistencia entre los módulos `core` y `tests`.

---

### Removed (Cambios en 0.9.1)

- Eliminados los **tests smoke** (`test_core_smoke.py` y `test_smoke_unittest.py`), ya que fueron reemplazados por pruebas unitarias específicas más completas.
- Eliminado código duplicado o no referenciado en módulos antiguos tras la integración de la Task-17.

---

### Fixed (Cambios en 0.9.1)

- Corrección de errores menores en condiciones lógicas de `Board.move_checker`.
- Ajuste en la validación del color en `Checker.__init__` que podía aceptar valores no válidos.
- Se evitó la creación de instancias de `Player` con listas mutables compartidas.
- Validación de longitud correcta de puntos (`points_status`) en `Board`.
- Ajuste de imports relativos rotos tras el merge anterior.

---

## [0.9.0] - 2025-10-01

### Added (Nuevas características en 0.9.0)

- **CLI (Command Line Interface):**
  - Nuevo archivo `cli/cli.py` que permite ejecutar partidas completas desde la consola.
  - Flujo interactivo para ingresar movimientos (`from_position to_position`) y salir del juego con `quit`.
  - Integración con la clase `Game` para mostrar el estado del tablero y el turno del jugador actual.

- **Core Game Logic:**
  - Implementación final de las clases principales del juego:
    - **`Board`**: ahora incluye lógica completa para mover fichas (`move_checker`), capturar, liberar y detectar bloqueos.
    - **`Checker`**: fichas con atributos privados (`__color__`, `__position__`, `__is_captured__`), y métodos para moverse o ser enviadas al “bar”.
    - **`Dice`**: sistema de dados con métodos `roll()`, `get_values()` y `is_double()` para gestionar tiradas reales y dobles.
    - **`Player`**: jugador con control de fichas, bar, home y lista de movimientos.
    - **`Game`**: clase principal que gestiona el flujo de turnos, validaciones, estados de partida y ganador.
  - Creación del módulo `exceptions.py` con excepciones específicas para el juego (`InvalidMoveException`, `NoAvailableMovesException`, etc.).

- **Testing Framework:**
  - Integración de `pytest` y creación de tests modulares por componente:
    - `test_board.py`
    - `test_checker.py`
    - `test_dice.py`
    - `test_game.py`
    - `test_player.py`
  - Tests diseñados con estructura unitaria clara, validando tanto inicialización como comportamiento dinámico (movimientos, turnos, capturas).
  - Implementación del archivo `test_smoke_unittest.py` para pruebas de integración generales.

- **Prompts Documentation:**
  - Expansión del archivo `prompts-testing.md` con documentación detallada del flujo IA y estructura de generación de código.
  - Nuevas secciones para trazabilidad de prompts, resultados de generación y registro de versiones de código IA.

---

### Changed (Cambios en 0.9.0)

- Refactorización completa de los módulos del core para estandarizar nombres, encapsular atributos y limpiar imports.
- Eliminación de código redundante previo y sustitución por clases funcionales finales.
- Revisión de métodos y docstrings para unificar estilo y claridad.
- Integración entre `core/` y `cli/` consolidada, con flujo estable y ejecución sin errores.
- Estandarización de las rutas de pruebas para el *coverage* de GitHub Actions.

---

### Fixed (Correcciones en 0.9.0)

- Resolución de conflictos de *coverage* que impedían el merge en CI/CD.
- Corrección de atributos no inicializados en `Player` y `Board`.
- Ajuste de errores lógicos en la detección de movimientos válidos y condiciones de victoria.
- Normalización de variables privadas con doble subrayado para evitar conflictos entre clases.

---

## [0.8.0] - 2025-09-30

### Changed (Cambios en 0.8.0)

- Reescritura completa de la estructura base del código en los módulos principales:
  - **`core/board.py`**:
    - Rediseño de la clase `Board` para incluir atributos más claros y privados:
      - `__points__`: lista de 24 posiciones del tablero.
      - `__captured__`: registro de fichas capturadas por color.
      - `__home__`: fichas que ya salieron del tablero.
    - Método `_setup_initial_position()` reorganizado con inicialización más explícita y coherente.
  - **`core/dice.py`**:
    - Sustitución de la función suelta `get_dice()` por una clase **`Dice`** completamente encapsulada.
    - Implementación de métodos:
      - `roll()`: simula el lanzamiento de los dados.
      - `get_values()`: devuelve los resultados actuales.
      - `is_double()`: detecta lanzamientos dobles.
  - **`core/player.py`**:
    - Actualización de la clase `Player` para adecuarla a la nueva estructura de `Dice` y `Board`.
    - Corrección de métodos y docstrings para mayor claridad y consistencia.

### Removed (Eliminado en 0.8.0)

- Código anterior de generación de dados y estructura del tablero basado en funciones sueltas.
- Comentarios y trazas de rutas locales de desarrollo (`C:\Users\Rufda...`), reemplazados por imports relativos limpios.

---

## [0.7.0] - 2025-09-20

### Added (Nuevas características en 0.7.0)

- Estructuración del directorio `tests/` con archivos individuales por módulo:
  - `test_board.py`
  - `test_dice.py`
  - `test_exceptions.py`
  - `test_game.py`
  - `test_player.py`
- Preparación de la base para futuras pruebas unitarias detalladas en cada componente principal del juego.
- Merge del branch `Task-15-estructura-de-tests-y-revision` a `main`.

### Changed (Cambios en 0.7.0)

- Eliminación progresiva del uso de *smoke tests* genéricos, reemplazados por estructura modular.
- Revisión de nombres de archivos y consistencia de formato en la carpeta `tests/`.
- Ajustes menores de estilo y comentarios en los nuevos archivos de prueba (sin cambios funcionales).

---

## [0.6.0] - 2025-09-14

### Added (Nuevas características en 0.6.0)

- Implementación del sistema de **Integración Continua (CI)** con GitHub Actions:
  - Configuración del archivo `.github/workflows/ci.yml` para ejecutar:
    - Instalación automática de dependencias.
    - Ejecución de pruebas unitarias (`unittest`) con generación de reportes de cobertura (`coverage`).
    - Análisis de calidad de código con `pylint`.
    - Creación automática de reportes y *pull requests* de resultados (`REPORTS.md`).
- Incorporación de archivo de configuración `.pylintrc` con parámetros personalizados (máximo de argumentos, ramas, métodos públicos, etc.).
- Añadidos **tests smoke** iniciales en la carpeta `tests/` para asegurar compatibilidad con la cobertura:
  - `test_core_smoke.py`
  - `test_smoke_unittest.py`
- Actualización del archivo `README.md` con el título **Backgammon 2025** y metadatos del proyecto.
- Documentación actualizada en `prompts-desarrollo.md` sobre la estructura del tablero (`Board`) y su proceso de generación.
- Merge del branch `Task-12-implementacion-de-integracion-continua` a `main`.

### Changed (Cambios en 0.6.0)

- Ajustes menores en los archivos de `prompts` para alinearlos con la nueva estructura.
- Revisión y adaptación de soluciones generadas por IA para mantener consistencia en el estilo del código y comentarios.
- Organización de carpetas internas (`prompts/` y `tests/`) para integrarse con el flujo de CI.

---

## [0.5.0] - 2025-09-13

### Added (Nuevas características en 0.5.0)

- Implementación de nuevas clases principales del juego:
  - **Dice**: define la función `get_dice()` para simular el lanzamiento de dados, incluyendo la regla especial de dobles.
  - **Game**: clase central que conecta tablero y jugadores, controlando el flujo de la partida.
  - **Player**: representa a cada jugador, con atributos `__name__`, `__color__`, `__pieces__` y `__bar__`.
- Nuevos métodos agregados en `Game`:
  - `switch_turn()`: alterna el turno entre jugadores.
  - `move()`: ejecuta movimientos válidos y actualiza el estado del tablero.
  - `check_winner()`: verifica si un jugador ganó.
  - `reset()`: reinicia la partida.
- Documentación detallada añadida en:
  - `prompts-desarrollo.md`: registro del proceso de creación de clases.
  - `prompts-documentacion.md`: explicación del código fuente (e.g., función `get_dice()`).
- Merge del branch `10-implementacion-en-las-clases-dicegame-y-player-documentacion-en-prompts-y-correccion-de-atributos` a `main`.

### Changed (Cambios en 0.5.0)

- Refactorización de atributos en `Board` y `Checker` para seguir convención de nombres privados con doble guion bajo (`__atributo__`).
- Corrección de docstrings y mejoras en comentarios de las clases principales.
- Estructura del módulo `core/` reorganizada para integrar `game.py`, `player.py` y `dice.py`.

---

## [0.4.0] - 2025-09-11

### Added (Nuevas características en 0.4.0)

- Implementación de clases principales del juego:
  - **Board**: estructura base del tablero con 24 puntos (triángulos) y lógica inicial de posiciones.
  - **Checker**: clase que representa las fichas con atributos `color`, `position` e `is_captured`.
- Métodos añadidos en `Checker`:
  - `move_to()`: mueve una ficha a una nueva posición.
  - `capture()`: marca una ficha como capturada y la envía al “bar”.
- Documentación generada mediante IA y buenas prácticas:
  - Archivos `prompts-desarrollo.md`, `prompts-documentacion.md` y `prompts-testing.md` para trazabilidad del desarrollo.
  - Archivo `copilot-instructions.md` con directrices de documentación y principios **SOLID**.
- Incorporación del documento `Backgammon Computacion 2025.pdf` como referencia del proyecto.
- Merge del branch `Task/implementacion-de-clases-en-boardpy-y-checkerpy-documentacion-en-prompts` a `main`.

### Changed (Cambios en 0.4.0)

- Estructura interna del módulo `core/` reorganizada para incluir docstrings y comentarios explicativos.
- Código documentado con convenciones claras de formato y responsabilidad única (principio SOLID).

---

## [0.3.0] - 2025-09-09

### Added (Nuevas características en 0.3.0)

- Creación del entorno virtual (`venv`) para el proyecto.
- Archivo `.gitignore` configurado para excluir:
  - Archivos compilados de Python (`__pycache__`, `.pyc`, `.pyo`, `.pyd`).
  - Directorios de distribución y dependencias (`build/`, `dist/`, `env/`, etc.).
- Incorporación del archivo `requirements.txt` con dependencias iniciales.
- Configuración básica para `coverage` y compatibilidad con GitHub Actions.
- Merge del branch `Task/creacion-de-venv-y-covenant` a `main`.

### Changed (Cambios en 0.3.0)

- Estructura de proyecto adaptada para incluir el entorno virtual y las reglas de exclusión.

---

## [0.2.0] - 2025-09-02

### Added (Nuevas características en 0.2.0) - Estructura de módulos

- Implementación inicial de las clases base en el módulo `core`:
  - `Board`, `Checker`, `Dice`, `Game` y `Player`.
- Merge del branch `4-creacion-de-clases` a `main`.
- Preparación de la estructura para definir la lógica del juego de Backgammon.

### Changed (Cambios en 0.2.0)

- Organización del código fuente bajo la carpeta `core/` para mantener separación por responsabilidad.

---

## [0.1.1] - 2025-08-30

### Added (Nuevas características en 0.1.1)

- Creación de la estructura de carpetas vacías para los módulos principales:
  - `core/`, `cli/`, `pygame_ui/` y `tests/`.
- Preparación del entorno base antes de la definición de clases.

---

## [0.1.0] - 2025-08-26

### Added

- Estructura inicial del proyecto creada a partir del branch `2-inicializar-repositorio-y-estructura-de-carpetas`.
- Directorios principales: `core/`, `cli/`, `pygame_ui/`, y `tests/`.
- Archivos base: `README.md`, `CHANGELOG.md`, `JUSTIFICACION.md`, y `requirements.txt`.
- Información inicial del alumno: *Augustus Rufino* – *Ingeniería Informática*.
