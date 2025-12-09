# Script para crear un usuario administrador inicial
Write-Host "👤 Creando usuario administrador inicial..." -ForegroundColor Cyan
Write-Host ""

$registerData = @{
    email = "admin@hotel.com"
    password = "admin123"
    first_name = "Admin"
    last_name = "Sistema"
    phone = "+123456789"
} | ConvertTo-Json

try {
    # Registrar usuario
    Write-Host "Registrando usuario..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
        -Method POST `
        -Body $registerData `
        -ContentType "application/json"
    
    Write-Host "✓ Usuario creado exitosamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "Credenciales:" -ForegroundColor White
    Write-Host "  Email: admin@hotel.com" -ForegroundColor Gray
    Write-Host "  Password: admin123" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Token de acceso:" -ForegroundColor White
    Write-Host "  $($response.access_token)" -ForegroundColor Gray
    Write-Host ""
    
    # Ahora convertir a admin (requiere acceso directo al User Service)
    Write-Host "Asignando rol de administrador..." -ForegroundColor Yellow
    
    $updateData = @{
        role = "admin"
    } | ConvertTo-Json
    
    $headers = @{
        "Authorization" = "Bearer $($response.access_token)"
    }
    
    # Obtener el user_id del token (simple decode - en producción usar JWT apropiado)
    # Por ahora asumimos que es el primer usuario (ID 1)
    $updateResponse = Invoke-RestMethod -Uri "http://localhost:8000/users/1" `
        -Method PUT `
        -Headers $headers `
        -Body $updateData `
        -ContentType "application/json"
    
    Write-Host "✓ Rol de administrador asignado" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Usuario administrador creado correctamente" -ForegroundColor Green
    
} catch {
    Write-Host "✗ Error al crear usuario: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Asegúrate de que:" -ForegroundColor Yellow
    Write-Host "  1. Todos los servicios están ejecutándose" -ForegroundColor White
    Write-Host "  2. El puerto 8000 (API Gateway) está accesible" -ForegroundColor White
    Write-Host "  3. Los servicios Auth y User están funcionando" -ForegroundColor White
}

Write-Host ""
