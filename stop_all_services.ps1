# Script para detener todos los procesos de microservicios
Write-Host "Deteniendo todos los microservicios..." -ForegroundColor Red
Write-Host ""

# Puertos de los servicios
$ports = @(8000, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008)

foreach ($port in $ports) {
    Write-Host "Buscando procesos en puerto $port..." -ForegroundColor Yellow
    
    # Buscar procesos usando el puerto
    $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"
    
    if ($connections) {
        foreach ($connection in $connections) {
            $parts = $connection -split '\s+'
            $processPid = $parts[-1]
            
            if ($processPid -and $processPid -ne "0") {
                $process = Get-Process -Id $processPid -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Host "  Deteniendo proceso $($process.Name) (PID: $processPid)" -ForegroundColor Green
                    Stop-Process -Id $processPid -Force -ErrorAction SilentlyContinue
                } else {
                    Write-Host "  No se pudo detener proceso con PID: $processPid" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "  - No hay procesos en puerto $port" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Limpieza completada" -ForegroundColor Green
Write-Host ""
