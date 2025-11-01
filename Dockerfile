# Dockerfile para Backgammon
# Este archivo define cómo construir la imagen Docker del juego

# Usar Python 3.11 como base (versión ligera)
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Juego de Backgammon con todas las reglas oficiales"

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto al contenedor
COPY . .

# Exponer puerto (por si en el futuro agregas interfaz web)
EXPOSE 8000

# Comando por defecto: ejecutar el CLI
CMD ["python", "-m", "cli.cli"]
