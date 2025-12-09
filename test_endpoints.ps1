# Script para probar todos los endpoints del sistema
Write-Host "=========================================="
Write-Host "PRUEBAS DE ENDPOINTS - Sistema Hotelero"
Write-Host "=========================================="
Write-Host ""

$ErrorActionPreference = "Continue"

# Variables globales
$token = ""
$userId = ""
$roomId = ""
$reservationId = ""
$menuItemId = ""
$tableId = ""
$restaurantReservationId = ""
$experienceId = ""

# Función para mostrar resultados
function Show-Result {
    param($ServiceName, $Endpoint, $Success, $Message)
    $status = if ($Success) { "[OK]" } else { "[ERROR]" }
    $color = if ($Success) { "Green" } else { "Red" }
    Write-Host "$status $ServiceName - $Endpoint" -ForegroundColor $color
    if ($Message) { Write-Host "      $Message" -ForegroundColor Gray }
}

Write-Host "==========================================";
Write-Host "1. API GATEWAY TESTS";
Write-Host "==========================================";

try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Show-Result "API Gateway" "GET /health" $true "Status: $($health.status)"
} catch {
    Show-Result "API Gateway" "GET /health" $false $_.Exception.Message
}

try {
    $services = Invoke-RestMethod -Uri "http://localhost:8000/services/status" -Method GET
    Show-Result "API Gateway" "GET /services/status" $true "All services checked"
} catch {
    Show-Result "API Gateway" "GET /services/status" $false $_.Exception.Message
}

Write-Host ""
Write-Host "==========================================";
Write-Host "2. AUTH SERVICE TESTS";
Write-Host "==========================================";

# Register new user
try {
    $registerBody = @{
        email = "testuser$(Get-Random)@hotel.com"
        password = "Test123!"
        first_name = "Test"
        last_name = "User"
        phone = "1234567890"
    } | ConvertTo-Json

    $registerResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/register" -Method POST -ContentType "application/json" -Body $registerBody
    $token = $registerResponse.access_token
    Show-Result "Auth Service" "POST /auth/register" $true "User registered successfully"
} catch {
    Show-Result "Auth Service" "POST /auth/register" $false $_.Exception.Message
}

# Login
try {
    $loginBody = @{
        email = "testuser@hotel.com"
        password = "Test123!"
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/login" -Method POST -ContentType "application/json" -Body $loginBody -ErrorAction SilentlyContinue
    if ($loginResponse.access_token) {
        $token = $loginResponse.access_token
        Show-Result "Auth Service" "POST /auth/login" $true "Login successful"
    }
} catch {
    Show-Result "Auth Service" "POST /auth/login" $false "User may not exist (OK if first run)"
}

# Verify token
if ($token) {
    try {
        $verifyBody = @{ token = $token } | ConvertTo-Json
        $verifyResponse = Invoke-RestMethod -Uri "http://localhost:8001/auth/verify" -Method POST -ContentType "application/json" -Body $verifyBody
        Show-Result "Auth Service" "POST /auth/verify" $true "Token is valid"
    } catch {
        Show-Result "Auth Service" "POST /auth/verify" $false $_.Exception.Message
    }
}

Write-Host ""
Write-Host "==========================================";
Write-Host "3. USER SERVICE TESTS";
Write-Host "==========================================";

# Get all users
try {
    $users = Invoke-RestMethod -Uri "http://localhost:8002/users/" -Method GET
    Show-Result "User Service" "GET /users/" $true "Found $($users.Count) users"
} catch {
    Show-Result "User Service" "GET /users/" $false $_.Exception.Message
}

# Create user
try {
    $createUserBody = @{
        email = "newuser$(Get-Random)@hotel.com"
        password = "Pass123!"
        first_name = "New"
        last_name = "User"
        phone = "9876543210"
        role = "user"
    } | ConvertTo-Json

    $newUser = Invoke-RestMethod -Uri "http://localhost:8002/users/" -Method POST -ContentType "application/json" -Body $createUserBody
    $userId = $newUser.id
    Show-Result "User Service" "POST /users/" $true "User created with ID: $userId"
} catch {
    Show-Result "User Service" "POST /users/" $false $_.Exception.Message
}

# Get user by ID
if ($userId) {
    try {
        $user = Invoke-RestMethod -Uri "http://localhost:8002/users/$userId" -Method GET
        Show-Result "User Service" "GET /users/{id}" $true "Retrieved user: $($user.email)"
    } catch {
        Show-Result "User Service" "GET /users/{id}" $false $_.Exception.Message
    }
}

Write-Host ""
Write-Host "==========================================";
Write-Host "4. ROOM SERVICE TESTS";
Write-Host "==========================================";

# Get all rooms
try {
    $rooms = Invoke-RestMethod -Uri "http://localhost:8003/rooms/" -Method GET
    Show-Result "Room Service" "GET /rooms/" $true "Found $($rooms.Count) rooms"
} catch {
    Show-Result "Room Service" "GET /rooms/" $false $_.Exception.Message
}

# Create room
try {
    $createRoomBody = @{
        room_number = "TEST-$(Get-Random -Maximum 999)"
        type = "Deluxe"
        price_per_night = 199.99
        capacity = 2
        amenities = @("WiFi", "TV", "Mini Bar")
        description = "Test room"
        is_available = $true
    } | ConvertTo-Json

    $newRoom = Invoke-RestMethod -Uri "http://localhost:8003/rooms/" -Method POST -ContentType "application/json" -Body $createRoomBody
    $roomId = $newRoom.id
    Show-Result "Room Service" "POST /rooms/" $true "Room created: $($newRoom.room_number)"
} catch {
    Show-Result "Room Service" "POST /rooms/" $false $_.Exception.Message
}

# Get room by ID
if ($roomId) {
    try {
        $room = Invoke-RestMethod -Uri "http://localhost:8003/rooms/$roomId" -Method GET
        Show-Result "Room Service" "GET /rooms/{id}" $true "Room: $($room.room_number)"
    } catch {
        Show-Result "Room Service" "GET /rooms/{id}" $false $_.Exception.Message
    }
}

# Get available rooms
try {
    $availableRooms = Invoke-RestMethod -Uri "http://localhost:8003/rooms/available" -Method GET
    Show-Result "Room Service" "GET /rooms/available" $true "Available rooms: $($availableRooms.Count)"
} catch {
    Show-Result "Room Service" "GET /rooms/available" $false $_.Exception.Message
}

Write-Host ""
Write-Host "==========================================";
Write-Host "5. ROOM RESERVATION SERVICE TESTS";
Write-Host "==========================================";

# Check availability
try {
    $checkInDate = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
    $checkOutDate = (Get-Date).AddDays(3).ToString("yyyy-MM-dd")
    
    $availability = Invoke-RestMethod -Uri "http://localhost:8004/reservations/check-availability?check_in_date=$checkInDate&check_out_date=$checkOutDate&guests_count=2" -Method GET
    Show-Result "Room Reservation" "GET /reservations/check-availability" $true "Available rooms found"
} catch {
    Show-Result "Room Reservation" "GET /reservations/check-availability" $false $_.Exception.Message
}

# Create reservation
if ($roomId) {
    try {
        $createReservationBody = @{
            user_id = 1
            room_id = $roomId
            check_in_date = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
            check_out_date = (Get-Date).AddDays(3).ToString("yyyy-MM-dd")
            guests_count = 2
            special_requests = "Test reservation"
        } | ConvertTo-Json

        $newReservation = Invoke-RestMethod -Uri "http://localhost:8004/reservations/" -Method POST -ContentType "application/json" -Body $createReservationBody
        $reservationId = $newReservation.id
        Show-Result "Room Reservation" "POST /reservations/" $true "Reservation created: $reservationId"
    } catch {
        Show-Result "Room Reservation" "POST /reservations/" $false $_.Exception.Message
    }
}

# Get all reservations
try {
    $reservations = Invoke-RestMethod -Uri "http://localhost:8004/reservations/" -Method GET
    Show-Result "Room Reservation" "GET /reservations/" $true "Found $($reservations.Count) reservations"
} catch {
    Show-Result "Room Reservation" "GET /reservations/" $false $_.Exception.Message
}

Write-Host ""
Write-Host "==========================================";
Write-Host "6. RESTAURANT SERVICE TESTS";
Write-Host "==========================================";

# Get menu items
try {
    $menuItems = Invoke-RestMethod -Uri "http://localhost:8005/menu/" -Method GET
    Show-Result "Restaurant Service" "GET /menu/" $true "Menu items: $($menuItems.Count)"
} catch {
    Show-Result "Restaurant Service" "GET /menu/" $false $_.Exception.Message
}

# Create menu item
try {
    $createMenuBody = @{
        name = "Test Dish $(Get-Random)"
        description = "Test description"
        category = "Main Course"
        price = 24.99
        is_available = $true
        allergens = @("Gluten")
    } | ConvertTo-Json

    $newMenuItem = Invoke-RestMethod -Uri "http://localhost:8005/menu/" -Method POST -ContentType "application/json" -Body $createMenuBody
    $menuItemId = $newMenuItem.id
    Show-Result "Restaurant Service" "POST /menu/" $true "Menu item created: $($newMenuItem.name)"
} catch {
    Show-Result "Restaurant Service" "POST /menu/" $false $_.Exception.Message
}

# Get tables
try {
    $tables = Invoke-RestMethod -Uri "http://localhost:8005/tables/" -Method GET
    Show-Result "Restaurant Service" "GET /tables/" $true "Tables: $($tables.Count)"
} catch {
    Show-Result "Restaurant Service" "GET /tables/" $false $_.Exception.Message
}

# Create table
try {
    $createTableBody = @{
        table_number = "T-$(Get-Random -Maximum 99)"
        capacity = 4
        location = "Terrace"
        is_available = $true
    } | ConvertTo-Json

    $newTable = Invoke-RestMethod -Uri "http://localhost:8005/tables/" -Method POST -ContentType "application/json" -Body $createTableBody
    $tableId = $newTable.id
    Show-Result "Restaurant Service" "POST /tables/" $true "Table created: $($newTable.table_number)"
} catch {
    Show-Result "Restaurant Service" "POST /tables/" $false $_.Exception.Message
}

Write-Host ""
Write-Host "==========================================";
Write-Host "7. RESTAURANT RESERVATION SERVICE TESTS";
Write-Host "==========================================";

# Get restaurant reservations
try {
    $restaurantReservations = Invoke-RestMethod -Uri "http://localhost:8006/restaurant-reservations/" -Method GET
    Show-Result "Restaurant Reservation" "GET /restaurant-reservations/" $true "Reservations: $($restaurantReservations.Count)"
} catch {
    Show-Result "Restaurant Reservation" "GET /restaurant-reservations/" $false $_.Exception.Message
}

# Create restaurant reservation
if ($tableId) {
    try {
        $createRestReservationBody = @{
            user_id = 1
            table_id = $tableId
            reservation_date = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
            reservation_time = "19:00:00"
            guests_count = 2
            special_requests = "Window seat"
        } | ConvertTo-Json

        $newRestReservation = Invoke-RestMethod -Uri "http://localhost:8006/restaurant-reservations/" -Method POST -ContentType "application/json" -Body $createRestReservationBody
        $restaurantReservationId = $newRestReservation.id
        Show-Result "Restaurant Reservation" "POST /restaurant-reservations/" $true "Reservation ID: $restaurantReservationId"
    } catch {
        Show-Result "Restaurant Reservation" "POST /restaurant-reservations/" $false $_.Exception.Message
    }
}

Write-Host ""
Write-Host "==========================================";
Write-Host "8. EXPERIENCE SERVICE TESTS";
Write-Host "==========================================";

# Get experiences
try {
    $experiences = Invoke-RestMethod -Uri "http://localhost:8007/experiences/" -Method GET
    Show-Result "Experience Service" "GET /experiences/" $true "Experiences: $($experiences.Count)"
} catch {
    Show-Result "Experience Service" "GET /experiences/" $false $_.Exception.Message
}

# Create experience
try {
    $createExperienceBody = @{
        user_id = 1
        title = "Test Experience"
        content = "This is a test review"
        rating = 5
        category = "Room"
        is_public = $true
    } | ConvertTo-Json

    $newExperience = Invoke-RestMethod -Uri "http://localhost:8007/experiences/" -Method POST -ContentType "application/json" -Body $createExperienceBody
    $experienceId = $newExperience.id
    Show-Result "Experience Service" "POST /experiences/" $true "Experience ID: $experienceId"
} catch {
    Show-Result "Experience Service" "POST /experiences/" $false $_.Exception.Message
}

# Get public experiences
try {
    $publicExperiences = Invoke-RestMethod -Uri "http://localhost:8007/experiences/public" -Method GET
    Show-Result "Experience Service" "GET /experiences/public" $true "Public experiences: $($publicExperiences.Count)"
} catch {
    Show-Result "Experience Service" "GET /experiences/public" $false $_.Exception.Message
}

Write-Host ""
Write-Host "==========================================";
Write-Host "9. ANALYTICS SERVICE TESTS";
Write-Host "==========================================";

# Get dashboard stats
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:8008/analytics/dashboard" -Method GET
    Show-Result "Analytics Service" "GET /analytics/dashboard" $true "Dashboard data retrieved"
} catch {
    Show-Result "Analytics Service" "GET /analytics/dashboard" $false $_.Exception.Message
}

# Get occupancy stats
try {
    $occupancy = Invoke-RestMethod -Uri "http://localhost:8008/analytics/occupancy" -Method GET
    Show-Result "Analytics Service" "GET /analytics/occupancy" $true "Occupancy: $($occupancy.current_occupancy_rate)%"
} catch {
    Show-Result "Analytics Service" "GET /analytics/occupancy" $false $_.Exception.Message
}

# Get revenue stats
try {
    $revenue = Invoke-RestMethod -Uri "http://localhost:8008/analytics/revenue" -Method GET
    Show-Result "Analytics Service" "GET /analytics/revenue" $true "Revenue data retrieved"
} catch {
    Show-Result "Analytics Service" "GET /analytics/revenue" $false $_.Exception.Message
}

# Get popular rooms
try {
    $popularRooms = Invoke-RestMethod -Uri "http://localhost:8008/analytics/popular-rooms" -Method GET
    Show-Result "Analytics Service" "GET /analytics/popular-rooms" $true "Popular rooms: $($popularRooms.Count)"
} catch {
    Show-Result "Analytics Service" "GET /analytics/popular-rooms" $false $_.Exception.Message
}

Write-Host ""
Write-Host "=========================================="
Write-Host "RESUMEN DE PRUEBAS COMPLETADO"
Write-Host "=========================================="
Write-Host ""
Write-Host "Todas las pruebas han sido ejecutadas." -ForegroundColor Cyan
Write-Host "Revisa los resultados arriba para ver el estado de cada endpoint." -ForegroundColor Cyan
Write-Host ""
