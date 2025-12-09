from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging
from .config import SERVICES, settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.GATEWAY_NAME,
    description="""
    API Gateway para el Sistema de Gestión Hotelera
    
    ## Servicios Disponibles
    
    - **auth** - Autenticación y autorización (Puerto 8001)
    - **users** - Gestión de usuarios (Puerto 8002)
    - **rooms** - Gestión de habitaciones (Puerto 8003)
    - **reservations** - Reservas de habitaciones (Puerto 8004)
    - **restaurant** - Gestión de restaurante (Puerto 8005)
    - **restaurant_reservations** - Reservas de restaurante (Puerto 8006)
    - **experiences** - Experiencias y reseñas (Puerto 8007)
    - **analytics** - Dashboard y estadísticas (Puerto 8008)
    
    ## Uso
    
    Todas las peticiones deben ir a: `http://localhost:8000/{servicio}/{ruta}`
    
    Ejemplo: `http://localhost:8000/auth/login`
    """,
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Endpoint raíz del API Gateway"""
    return {
        "service": settings.GATEWAY_NAME,
        "version": "1.0.0",
        "status": "running",
        "services": {
            "auth": f"{SERVICES['auth']}",
            "users": f"{SERVICES['users']}",
            "rooms": f"{SERVICES['rooms']}",
            "room_reservations": f"{SERVICES['room_reservations']}",
            "restaurant": f"{SERVICES['restaurant']}",
            "restaurant_reservations": f"{SERVICES['restaurant_reservations']}",
            "experiences": f"{SERVICES['experiences']}",
            "analytics": f"{SERVICES['analytics']}",
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "gateway": "operational"}


@app.get("/services/status")
async def check_services_status():
    """Verificar el estado de todos los microservicios"""
    status_dict = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health")
                status_dict[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_url,
                    "code": response.status_code
                }
            except Exception as e:
                status_dict[service_name] = {
                    "status": "unreachable",
                    "url": service_url,
                    "error": str(e)
                }
    
    return {"services": status_dict}


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    """
    Gateway principal que enruta las peticiones a los microservicios
    
    - **service**: Nombre del microservicio (auth, users, rooms, etc.)
    - **path**: Ruta específica del endpoint
    """
    # Verificar si el servicio existe
    if service not in SERVICES:
        logger.error(f"Servicio no encontrado: {service}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio '{service}' no encontrado. Servicios disponibles: {list(SERVICES.keys())}"
        )
    
    # Construir URL del servicio
    service_url = SERVICES[service]
    target_url = f"{service_url}/{path}"
    
    # Obtener query parameters
    query_params = str(request.url.query)
    if query_params:
        target_url += f"?{query_params}"
    
    logger.info(f"{request.method} {target_url}")
    
    try:
        # Preparar headers
        headers = dict(request.headers)
        # Remover headers problemáticos
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # Hacer la petición al microservicio
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
            )
        
        # Retornar la respuesta del microservicio
        return JSONResponse(
            status_code=response.status_code,
            content=response.json() if response.content else None,
            headers=dict(response.headers)
        )
    
    except httpx.TimeoutException:
        logger.error(f"Timeout al contactar {service_url}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Timeout al contactar el servicio '{service}'"
        )
    
    except httpx.RequestError as e:
        logger.error(f"Error al contactar {service_url}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Servicio '{service}' no disponible: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del gateway: {str(e)}"
        )


# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para registrar todas las peticiones"""
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.GATEWAY_PORT)
