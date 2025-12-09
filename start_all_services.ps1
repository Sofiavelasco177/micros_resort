# Script para iniciar todos los microservicios
# Sistema de Gestión Hotelera

Write-Host "Iniciando Sistema de Gestion Hotelera..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    exit 1
}

# Verificar si las dependencias están instaladas
Write-Host ""
Write-Host "Verificando dependencias..." -ForegroundColor Yellow

Write-Host "Instalando/actualizando dependencias..." -ForegroundColor Yellow
pip install -q -r requirements.txt
Write-Host "Dependencias instaladas" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Iniciando microservicios..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Array de servicios
$services = @(
    @{Name="Auth Service"; Path="auth_service"; Port=8001},
    @{Name="User Service"; Path="user_service"; Port=8002},
    @{Name="Room Service"; Path="room_service"; Port=8003},
    @{Name="Room Reservation Service"; Path="room_reservation_service"; Port=8004},
    @{Name="Restaurant Service"; Path="restaurant_service"; Port=8005},
    @{Name="Restaurant Reservation Service"; Path="restaurant_reservation_service"; Port=8006},
    @{Name="Experience Service"; Path="experience_service"; Port=8007},
    @{Name="Analytics Service"; Path="analytics_service"; Port=8008},
    @{Name="API Gateway"; Path="api_gateway"; Port=8000}
)

# Iniciar cada servicio en una nueva ventana de PowerShell
foreach ($service in $services) {
    Write-Host "Iniciando $($service.Name) en puerto $($service.Port)..." -ForegroundColor Green
    
    $command = "cd '$($service.Path)' ; uvicorn app.main:app --reload --port $($service.Port)"
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal
    
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Todos los servicios iniciados" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentacion disponible en:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  API Gateway:          http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Auth Service:         http://localhost:8001/docs" -ForegroundColor White
Write-Host "  User Service:         http://localhost:8002/docs" -ForegroundColor White
Write-Host "  Room Service:         http://localhost:8003/docs" -ForegroundColor White
Write-Host "  Room Reservation:     http://localhost:8004/docs" -ForegroundColor White
Write-Host "  Restaurant Service:   http://localhost:8005/docs" -ForegroundColor White
Write-Host "  Restaurant Reservation: http://localhost:8006/docs" -ForegroundColor White
Write-Host "  Experience Service:   http://localhost:8007/docs" -ForegroundColor White
Write-Host "  Analytics Service:    http://localhost:8008/docs" -ForegroundColor White
Write-Host ""
Write-Host "Usa Ctrl+C en cada ventana para detener los servicios" -ForegroundColor Cyan
Write-Host ""
