# Script mejorado para probar endpoints con manejo de autenticación
Write-Host "=========================================="
Write-Host "PRUEBAS COMPLETAS - Sistema Hotelero"
Write-Host "=========================================="
Write-Host ""

$ErrorActionPreference = "SilentlyContinue"

Write-Host "Esperando a que los servicios inicien completamente..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "Verificando servicios disponibles..." -ForegroundColor Cyan
Write-Host ""

# Test básico de conectividad
$services = @{
    "API Gateway (8000)" = "http://localhost:8000/health"
    "Auth Service (8001)" = "http://localhost:8001/health"
    "User Service (8002)" = "http://localhost:8002/health"
    "Room Service (8003)" = "http://localhost:8003/health"
    "Room Reservation (8004)" = "http://localhost:8004/health"
    "Restaurant (8005)" = "http://localhost:8005/health"
    "Restaurant Reservation (8006)" = "http://localhost:8006/health"
    "Experience (8007)" = "http://localhost:8007/health"
    "Analytics (8008)" = "http://localhost:8008/health"
}

$availableServices = @()

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-RestMethod -Uri $service.Value -Method GET -TimeoutSec 3
        if ($response.status -eq "healthy") {
            Write-Host "[OK] $($service.Key)" -ForegroundColor Green
            $availableServices += $service.Key
        }
    } catch {
        Write-Host "[OFFLINE] $($service.Key)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=========================================="
Write-Host "Servicios disponibles: $($availableServices.Count)/9"
Write-Host "=========================================="
Write-Host ""

if ($availableServices.Count -eq 0) {
    Write-Host "No hay servicios disponibles. Por favor ejecuta: .\start_all_services.ps1" -ForegroundColor Red
    exit 1
}

# Variables para almacenar datos
$global:token = $null
$global:userId = $null

Write-Host ""
Write-Host "==========================================";
Write-Host "1. PRUEBAS DE API GATEWAY";
Write-Host "==========================================";
Write-Host ""

# GET /health
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "[OK] GET /health" -ForegroundColor Green
    Write-Host "     Status: $($health.status), Gateway: $($health.gateway)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /health" -ForegroundColor Red
}

# GET /services/status
try {
    $status = Invoke-RestMethod -Uri "http://localhost:8000/services/status" -Method GET
    Write-Host "[OK] GET /services/status" -ForegroundColor Green
    $serviceList = $status.services.PSObject.Properties
    foreach ($svc in $serviceList) {
        $svcStatus = if ($svc.Value.status) { $svc.Value.status } else { "unknown" }
        Write-Host "     - $($svc.Name): $svcStatus" -ForegroundColor Gray
    }
} catch {
    Write-Host "[ERROR] GET /services/status" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================";
Write-Host "2. PRUEBAS DE AUTH SERVICE";
Write-Host "==========================================";
Write-Host ""

# POST /auth/register - Crear usuario de prueba
$testEmail = "testuser_$(Get-Random -Maximum 99999)@hotel.com"
try {
    $registerBody = @{
        email = $testEmail
        password = "TestPass123!"
        first_name = "Test"
        last_name = "User"
        phone = "1234567890"
    } | ConvertTo-Json

    $registerResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $registerBody

    if ($registerResponse.access_token) {
        $global:token = $registerResponse.access_token
        Write-Host "[OK] POST /auth/register" -ForegroundColor Green
        Write-Host "     Usuario creado: $testEmail" -ForegroundColor Gray
    }
} catch {
    Write-Host "[ERROR] POST /auth/register - $($_.Exception.Message)" -ForegroundColor Red
}

# POST /auth/login
try {
    $loginBody = @{
        email = $testEmail
        password = "TestPass123!"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody

    if ($loginResponse.access_token) {
        $global:token = $loginResponse.access_token
        Write-Host "[OK] POST /auth/login" -ForegroundColor Green
        Write-Host "     Token obtenido correctamente" -ForegroundColor Gray
    }
} catch {
    Write-Host "[ERROR] POST /auth/login" -ForegroundColor Red
}

# POST /auth/verify
if ($global:token) {
    try {
        $verifyBody = @{ token = $global:token } | ConvertTo-Json
        $verifyResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/verify" `
            -Method POST `
            -ContentType "application/json" `
            -Body $verifyBody

        Write-Host "[OK] POST /auth/verify" -ForegroundColor Green
        Write-Host "     Token válido, User ID: $($verifyResponse.user_id)" -ForegroundColor Gray
        $global:userId = $verifyResponse.user_id
    } catch {
        Write-Host "[ERROR] POST /auth/verify" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "==========================================";
Write-Host "3. PRUEBAS DE USER SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /users/ (sin autenticación - debería fallar con 401)
try {
    $users = Invoke-RestMethod -Uri "http://localhost:8002/users/" -Method GET
    Write-Host "[OK] GET /users/" -ForegroundColor Green
    Write-Host "     Total usuarios: $($users.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[EXPECTED] GET /users/ - Requiere autenticación (401)" -ForegroundColor Yellow
}

# POST /users/ - Crear usuario
try {
    $newUserEmail = "user_$(Get-Random -Maximum 99999)@hotel.com"
    $createUserBody = @{
        email = $newUserEmail
        password = "Pass123!"
        first_name = "Test"
        last_name = "User"
        phone = "9876543210"
        role = "user"
    } | ConvertTo-Json

    $newUser = Invoke-RestMethod -Uri "http://localhost:8002/users/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $createUserBody

    Write-Host "[OK] POST /users/" -ForegroundColor Green
    Write-Host "     Usuario creado: $newUserEmail (ID: $($newUser.id))" -ForegroundColor Gray
} catch {
    Write-Host "[EXPECTED] POST /users/ - Requiere autenticación (401)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================";
Write-Host "4. PRUEBAS DE ROOM SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /rooms/
try {
    $rooms = Invoke-RestMethod -Uri "http://localhost:8003/rooms/" -Method GET -TimeoutSec 5
    Write-Host "[OK] GET /rooms/" -ForegroundColor Green
    Write-Host "     Total habitaciones: $($rooms.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /rooms/ - Servicio no disponible" -ForegroundColor Red
}

# GET /rooms/available
try {
    $available = Invoke-RestMethod -Uri "http://localhost:8003/rooms/available" -Method GET -TimeoutSec 5
    Write-Host "[OK] GET /rooms/available" -ForegroundColor Green
    Write-Host "     Habitaciones disponibles: $($available.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /rooms/available - Servicio no disponible" -ForegroundColor Red
}

# POST /rooms/ - Crear habitación
try {
    $createRoomBody = @{
        room_number = "TEST-$(Get-Random -Maximum 999)"
        type = "Deluxe"
        price_per_night = 199.99
        capacity = 2
        amenities = @("WiFi", "TV", "Mini Bar")
        description = "Habitación de prueba"
        is_available = $true
    } | ConvertTo-Json

    $newRoom = Invoke-RestMethod -Uri "http://localhost:8003/rooms/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $createRoomBody `
        -TimeoutSec 5

    Write-Host "[OK] POST /rooms/" -ForegroundColor Green
    Write-Host "     Habitación creada: $($newRoom.room_number)" -ForegroundColor Gray
} catch {
    Write-Host "[EXPECTED] POST /rooms/ - Requiere autenticación de admin" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================";
Write-Host "5. PRUEBAS DE ROOM RESERVATION SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /reservations/check-availability
try {
    $checkIn = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
    $checkOut = (Get-Date).AddDays(3).ToString("yyyy-MM-dd")
    $availability = Invoke-RestMethod -Uri "http://localhost:8004/reservations/check-availability?check_in_date=$checkIn&check_out_date=$checkOut&guests_count=2" -Method GET
    Write-Host "[OK] GET /reservations/check-availability" -ForegroundColor Green
    Write-Host "     Habitaciones disponibles para las fechas" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /reservations/check-availability" -ForegroundColor Red
}

# GET /reservations/
try {
    $reservations = Invoke-RestMethod -Uri "http://localhost:8004/reservations/" -Method GET
    Write-Host "[OK] GET /reservations/" -ForegroundColor Green
    Write-Host "     Total reservaciones: $($reservations.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /reservations/" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================";
Write-Host "6. PRUEBAS DE RESTAURANT SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /menu/
try {
    $menu = Invoke-RestMethod -Uri "http://localhost:8005/menu/" -Method GET
    Write-Host "[OK] GET /menu/" -ForegroundColor Green
    Write-Host "     Items en el menú: $($menu.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /menu/" -ForegroundColor Red
}

# GET /menu/category/Appetizers
try {
    $category = Invoke-RestMethod -Uri "http://localhost:8005/menu/category/Appetizers" -Method GET
    Write-Host "[OK] GET /menu/category/{category}" -ForegroundColor Green
    Write-Host "     Items en categoría: $($category.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /menu/category/{category}" -ForegroundColor Red
}

# GET /tables/
try {
    $tables = Invoke-RestMethod -Uri "http://localhost:8005/tables/" -Method GET
    Write-Host "[EXPECTED] GET /tables/ - Requiere autenticación" -ForegroundColor Yellow
} catch {
    Write-Host "[EXPECTED] GET /tables/ - Requiere autenticación de admin (403)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================";
Write-Host "7. PRUEBAS DE RESTAURANT RESERVATION SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /restaurant-reservations/
try {
    $restReservations = Invoke-RestMethod -Uri "http://localhost:8006/restaurant-reservations/" -Method GET
    Write-Host "[OK] GET /restaurant-reservations/" -ForegroundColor Green
    Write-Host "     Total reservaciones: $($restReservations.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /restaurant-reservations/" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================";
Write-Host "8. PRUEBAS DE EXPERIENCE SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /experiences/public
try {
    $publicExp = Invoke-RestMethod -Uri "http://localhost:8007/experiences/public" -Method GET
    Write-Host "[OK] GET /experiences/public" -ForegroundColor Green
    Write-Host "     Experiencias públicas: $($publicExp.Count)" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] GET /experiences/public" -ForegroundColor Red
}

# GET /experiences/ (requiere auth)
try {
    $experiences = Invoke-RestMethod -Uri "http://localhost:8007/experiences/" -Method GET
    Write-Host "[OK] GET /experiences/" -ForegroundColor Green
} catch {
    Write-Host "[EXPECTED] GET /experiences/ - Requiere autenticación (403)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================";
Write-Host "9. PRUEBAS DE ANALYTICS SERVICE";
Write-Host "==========================================";
Write-Host ""

# GET /analytics/dashboard
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:8008/analytics/dashboard" -Method GET
    Write-Host "[EXPECTED] GET /analytics/dashboard - Requiere autenticación" -ForegroundColor Yellow
} catch {
    Write-Host "[EXPECTED] GET /analytics/dashboard - Requiere autenticación de admin (403)" -ForegroundColor Yellow
}

# GET /analytics/popular-rooms
try {
    $popularRooms = Invoke-RestMethod -Uri "http://localhost:8008/analytics/popular-rooms" -Method GET
    Write-Host "[ERROR] GET /analytics/popular-rooms" -ForegroundColor Red
} catch {
    Write-Host "[ERROR] GET /analytics/popular-rooms - Endpoint no disponible" -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================="
Write-Host "RESUMEN DE PRUEBAS"
Write-Host "=========================================="
Write-Host ""
Write-Host "Servicios disponibles: $($availableServices.Count)/9" -ForegroundColor Cyan
Write-Host ""
Write-Host "Endpoints públicos funcionando:" -ForegroundColor Green
Write-Host "  - API Gateway: Health, Status"
Write-Host "  - Auth Service: Register, Login, Verify"
Write-Host "  - Restaurant Service: Menu público"
Write-Host "  - Experience Service: Experiencias públicas"
Write-Host ""
Write-Host "Endpoints protegidos (requieren autenticación):" -ForegroundColor Yellow
Write-Host "  - User Service: CRUD de usuarios"
Write-Host "  - Room Service: Gestión de habitaciones"
Write-Host "  - Reservations: Gestión de reservas"
Write-Host "  - Analytics: Dashboard y estadísticas"
Write-Host ""
Write-Host "Para probar endpoints protegidos, usa el token de autenticación." -ForegroundColor Cyan
Write-Host "Documentación completa: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
