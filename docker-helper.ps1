# Script de PowerShell para facilitar el uso de Docker con Backgammon
# Ejecutar: .\docker-helper.ps1 [comando]

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "`n=== 🐳 Docker Helper para Backgammon ===" -ForegroundColor Cyan
    Write-Host "`nComandos disponibles:" -ForegroundColor Yellow
    Write-Host "  .\docker-helper.ps1 build       - Construir imagen Docker"
    Write-Host "  .\docker-helper.ps1 play        - Jugar al Backgammon"
    Write-Host "  .\docker-helper.ps1 test        - Ejecutar tests"
    Write-Host "  .\docker-helper.ps1 coverage    - Ver cobertura de código"
    Write-Host "  .\docker-helper.ps1 clean       - Limpiar contenedores e imágenes"
    Write-Host "  .\docker-helper.ps1 status      - Ver estado de Docker"
    Write-Host "  .\docker-helper.ps1 shell       - Abrir shell interactiva en contenedor"
    Write-Host "`n"
}

function Test-Docker {
    try {
        docker --version | Out-Null
        return $true
    }
    catch {
        Write-Host "❌ ERROR: Docker no está instalado o no está en el PATH" -ForegroundColor Red
        Write-Host "   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        return $false
    }
}

function Build-Image {
    Write-Host "`n🔨 Construyendo imagen Docker..." -ForegroundColor Cyan
    docker-compose build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Imagen construida exitosamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al construir la imagen" -ForegroundColor Red
    }
}

function Play-Game {
    Write-Host "`n🎮 Iniciando Backgammon..." -ForegroundColor Cyan
    docker-compose run --rm backgammon-cli
}

function Run-Tests {
    Write-Host "`n🧪 Ejecutando tests..." -ForegroundColor Cyan
    docker-compose run --rm backgammon-tests
}

function Run-Coverage {
    Write-Host "`n📊 Ejecutando cobertura de código..." -ForegroundColor Cyan
    docker-compose run --rm backgammon-coverage
}

function Clean-Docker {
    Write-Host "`n🧹 Limpiando Docker..." -ForegroundColor Cyan
    
    Write-Host "  - Deteniendo contenedores..." -ForegroundColor Yellow
    docker-compose down
    
    Write-Host "  - Eliminando contenedores detenidos..." -ForegroundColor Yellow
    docker container prune -f
    
    Write-Host "  - Eliminando imagen del proyecto..." -ForegroundColor Yellow
    docker rmi backgammon-game:latest -f
    
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Show-Status {
    Write-Host "`n📊 Estado de Docker" -ForegroundColor Cyan
    
    Write-Host "`nImágenes:" -ForegroundColor Yellow
    docker images | Select-String "backgammon|REPOSITORY"
    
    Write-Host "`nContenedores activos:" -ForegroundColor Yellow
    docker ps | Select-String "backgammon|CONTAINER"
    
    Write-Host "`nContenedores detenidos:" -ForegroundColor Yellow
    docker ps -a | Select-String "backgammon|CONTAINER"
}

function Open-Shell {
    Write-Host "`n🐚 Abriendo shell interactiva..." -ForegroundColor Cyan
    docker run -it --rm -v ${PWD}:/app backgammon-game:latest /bin/bash
}

# Main
if (-not (Test-Docker)) {
    exit 1
}

switch ($Command.ToLower()) {
    "build"    { Build-Image }
    "play"     { Play-Game }
    "test"     { Run-Tests }
    "coverage" { Run-Coverage }
    "clean"    { Clean-Docker }
    "status"   { Show-Status }
    "shell"    { Open-Shell }
    "help"     { Show-Help }
    default    { 
        Write-Host "❌ Comando desconocido: $Command" -ForegroundColor Red
        Show-Help 
    }
}
