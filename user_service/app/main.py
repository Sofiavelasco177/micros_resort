from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import init_db
from .api.routes import router
from .config import settings

app = FastAPI(
    title=settings.SERVICE_NAME,
    description="Servicio de gestión de usuarios para el sistema hotelero",
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

# Incluir routers
app.include_router(router)


@app.on_event("startup")
def startup_event():
    """Inicializar base de datos al arrancar"""
    init_db()


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "service": settings.SERVICE_NAME,
        "status": "running",
        "port": settings.SERVICE_PORT
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
