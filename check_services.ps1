# Script para verificar el estado de todos los microservicios
Write-Host "Verificando estado de microservicios..." -ForegroundColor Cyan
Write-Host ""

$services = @(
    @{Name="API Gateway"; URL="http://localhost:8000/health"},
    @{Name="Auth Service"; URL="http://localhost:8001/health"},
    @{Name="User Service"; URL="http://localhost:8002/health"},
    @{Name="Room Service"; URL="http://localhost:8003/health"},
    @{Name="Room Reservation"; URL="http://localhost:8004/health"},
    @{Name="Restaurant Service"; URL="http://localhost:8005/health"},
    @{Name="Restaurant Reservation"; URL="http://localhost:8006/health"},
    @{Name="Experience Service"; URL="http://localhost:8007/health"},
    @{Name="Analytics Service"; URL="http://localhost:8008/health"}
)

$healthy = 0
$unhealthy = 0

foreach ($service in $services) {
    $response = Invoke-WebRequest -Uri $service.URL -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response -and $response.StatusCode -eq 200) {
        Write-Host "[OK] $($service.Name.PadRight(30)) [HEALTHY]" -ForegroundColor Green
        $healthy++
    } else {
        Write-Host "[ERROR] $($service.Name.PadRight(30)) [OFFLINE]" -ForegroundColor Red
        $unhealthy++
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Resumen:" -ForegroundColor White
Write-Host "  Servicios saludables: $healthy" -ForegroundColor Green
Write-Host "  Servicios con problemas: $unhealthy" -ForegroundColor $(if ($unhealthy -gt 0) { "Red" } else { "Gray" })
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($healthy -eq 9) {
    Write-Host "Todos los servicios estan funcionando correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Accede a la documentacion en: http://localhost:8000/docs" -ForegroundColor Cyan
} else {
    Write-Host "Algunos servicios no estan disponibles" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verifica que todos los servicios esten iniciados con:" -ForegroundColor White
    Write-Host "  .\start_all_services.ps1" -ForegroundColor Gray
}

Write-Host ""
