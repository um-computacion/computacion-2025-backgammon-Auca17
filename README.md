# Backgammon

Un juego de Backgammon implementado en Python con dos interfaces: una gráfica con Pygame y otra de línea de comandos.

**Alumno:** Augustus Rufino

---

## Prerrequisitos

Asegúrate de tener Python instalado en tu sistema. Se recomienda usar **Python 3.8** o una versión superior.

### 1. Crear Entorno Virtual

Para mantener las dependencias aisladas, crea un entorno virtual:

```bash
python -m venv .venv
```

### 2. Activar Entorno Virtual

Una vez creado, actívalo. El comando puede variar según tu sistema operativo y terminal:

* **En Windows (usando Git Bash o similar):**

    ```bash
    source .venv/Scripts/activate
    ```

* **En Windows (usando Command Prompt o PowerShell):**

    ```bash
    .venv\Scripts\activate
    ```

* **En macOS / Linux:**

    ```bash
    source .venv/bin/activate
    ```

### 3. Instalar Dependencias (previo activar el entorno virtual)

Con el entorno virtual activado, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## Cómo Jugar

Este proyecto incluye dos formas de jugar: una interfaz gráfica y una interfaz de línea de comandos.

### Interfaz Gráfica (Pygame)

Para iniciar la versión visual del juego, ejecuta el siguiente comando:

```bash
python -m pygame_ui.main
```

### Interfaz de Línea de Comandos (CLI)

Para jugar en la terminal, utiliza este comando:

```bash
python -m cli.cli
```

---

## Uso de la Interfaz Gráfica (Pygame)

La interfaz gráfica ofrece una experiencia visual completa. El flujo del juego es el siguiente:

1. **Menú Principal**: Inicia seleccionando "Jugador vs Jugador".
2. **Entrada de Nombres**: Introduce los nombres para ambos jugadores.
3. **Tirada Inicial**: La pantalla mostrará una tirada de un dado por jugador para decidir quién empieza. Presiona la barra espaciadora para continuar.
4. **Juego Principal**: ¡Empieza a jugar!

### Controles

* **Clic del Ratón**:
  * Haz clic en una de tus fichas para seleccionarla (se resaltará).
  * Haz clic en un punto de destino válido para mover la ficha.
* **Barra Espaciadora**: Úsala al inicio de tu turno para tirar los dados.
* **Tecla R**: Presiónala en cualquier momento durante la partida para reiniciar el juego y volver al menú principal.

---

## Uso de la Interfaz de Comandos (CLI)

La versión CLI es ideal para jugar en un entorno de texto. El juego te guiará a través de los pasos:

1. **Nombres de Jugadores**: El juego te pedirá que introduzcas los nombres de ambos jugadores al inicio.
2. **Tirada Inicial**: Se realizará una tirada automática para decidir quién comienza.
3. **Juego Principal**: El juego mostrará el tablero, la tirada de dados y una lista de todos los movimientos posibles en cada turno.

### Comandos

* **Hacer un Movimiento**: Cuando se te pida, introduce tu movimiento con el formato `desde hasta`. Por ejemplo, para mover una ficha del punto 18 al 23, escribe:

    ``` text
    18 23
    ```

* **Salir del Juego**: Para terminar la partida en cualquier momento, escribe `salir` y presiona Enter.
