# Hotel Management Microservices System
# Test Data Setup Script

Write-Host "📦 Configurando datos de prueba..." -ForegroundColor Cyan
Write-Host ""

# Esperar a que los servicios estén listos
Write-Host "Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 1. Crear usuario admin
Write-Host "1. Creando usuario administrador..." -ForegroundColor Yellow
$adminRegister = @{
    email = "admin@hotel.com"
    password = "admin123"
    first_name = "Admin"
    last_name = "Sistema"
} | ConvertTo-Json

try {
    $adminResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
        -Method POST -Body $adminRegister -ContentType "application/json"
    $adminToken = $adminResponse.access_token
    Write-Host "   ✓ Admin creado" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Admin ya existe o error" -ForegroundColor Yellow
    # Intentar login
    $loginData = @{email="admin@hotel.com"; password="admin123"} | ConvertTo-Json
    $adminResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
        -Method POST -Body $loginData -ContentType "application/json"
    $adminToken = $adminResponse.access_token
}

$headers = @{"Authorization" = "Bearer $adminToken"}

# 2. Crear habitaciones
Write-Host "2. Creando habitaciones..." -ForegroundColor Yellow
$rooms = @(
    @{room_number="101"; type="single"; price_per_night=50; capacity=1; description="Habitación individual"; amenities=@("wifi","tv")},
    @{room_number="201"; type="double"; price_per_night=80; capacity=2; description="Habitación doble"; amenities=@("wifi","tv","minibar")},
    @{room_number="301"; type="suite"; price_per_night=150; capacity=4; description="Suite ejecutiva"; amenities=@("wifi","tv","minibar","balcony")},
    @{room_number="401"; type="deluxe"; price_per_night=250; capacity=4; description="Habitación deluxe"; amenities=@("wifi","tv","minibar","balcony","jacuzzi")}
)

foreach ($room in $rooms) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/rooms/" `
            -Method POST -Headers $headers -Body ($room | ConvertTo-Json) -ContentType "application/json" | Out-Null
        Write-Host "   ✓ Habitación $($room.room_number) creada" -ForegroundColor Green
    } catch {}
}

# 3. Crear items de menú
Write-Host "3. Creando menú del restaurante..." -ForegroundColor Yellow
$menuItems = @(
    @{name="Ensalada César"; description="Ensalada fresca"; category="appetizer"; price=12; allergens=@("gluten")},
    @{name="Filet Mignon"; description="Carne premium"; category="main"; price=35; allergens=@()},
    @{name="Salmón al horno"; description="Pescado fresco"; category="main"; price=28; allergens=@("fish")},
    @{name="Tiramisú"; description="Postre italiano"; category="dessert"; price=8; allergens=@("gluten","dairy")},
    @{name="Agua mineral"; description="500ml"; category="beverage"; price=3; allergens=@()}
)

foreach ($item in $menuItems) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/restaurant/menu/" `
            -Method POST -Headers $headers -Body ($item | ConvertTo-Json) -ContentType "application/json" | Out-Null
        Write-Host "   ✓ $($item.name) agregado" -ForegroundColor Green
    } catch {}
}

# 4. Crear mesas del restaurante
Write-Host "4. Creando mesas del restaurante..." -ForegroundColor Yellow
$tables = @(
    @{table_number="T1"; capacity=2; location="indoor"},
    @{table_number="T2"; capacity=4; location="indoor"},
    @{table_number="T3"; capacity=6; location="indoor"},
    @{table_number="T4"; capacity=2; location="terrace"},
    @{table_number="T5"; capacity=4; location="window"}
)

foreach ($table in $tables) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/restaurant/tables/" `
            -Method POST -Headers $headers -Body ($table | ConvertTo-Json) -ContentType "application/json" | Out-Null
        Write-Host "   ✓ Mesa $($table.table_number) creada" -ForegroundColor Green
    } catch {}
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ Datos de prueba configurados" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales de admin:" -ForegroundColor White
Write-Host "  Email: admin@hotel.com" -ForegroundColor Gray
Write-Host "  Password: admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "Datos creados:" -ForegroundColor White
Write-Host "  - 4 habitaciones (101, 201, 301, 401)" -ForegroundColor Gray
Write-Host "  - 5 items del menú" -ForegroundColor Gray
Write-Host "  - 5 mesas del restaurante" -ForegroundColor Gray
Write-Host ""
Write-Host "Accede a la documentación: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
