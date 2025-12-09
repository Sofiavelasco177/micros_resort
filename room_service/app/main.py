from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import init_db
from .api.routes import router
from .config import settings

app = FastAPI(
    title=settings.SERVICE_NAME,
    description="Servicio de gestión de habitaciones e inventario",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"service": settings.SERVICE_NAME, "status": "running", "port": settings.SERVICE_PORT}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
