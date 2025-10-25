# Changelog

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

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

### Changed (Modificaciones en 1.1.0)

- `Game.display_board()` ahora imprime directamente la representación generada por `Board.get_2d_representation()`.
- `Board.move_checker()` optimizado para manejo de errores y extracción controlada de fichas.
- `cli.main()` reorganizado:
  - Agregada gestión de listas de movimientos posibles antes de la solicitud de entrada.
  - Eliminadas comprobaciones redundantes de `get_dice_values()` en favor de `get_possible_moves()`.
- Estructura de los mensajes del CLI reformulada para mayor claridad en la interacción con el jugador.

### Fixed (Correcciones en 1.1.0)

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

### Fixed (Correcciones en 1.0.0)

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
