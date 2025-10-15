# Changelog

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

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
