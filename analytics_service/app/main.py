from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import router
from .database.connection import init_db

app = FastAPI(
    title=settings.SERVICE_NAME,
    version="1.0.0",
    description="Analytics Service for Hotel Management System"
)

# Inicializar base de datos al arrancar
@app.on_event("startup")
def startup_event():
    init_db()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
def root():
    return {
        "service": settings.SERVICE_NAME,
        "status": "running",
        "port": settings.SERVICE_PORT
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
