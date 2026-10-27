from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from models import user_model
from api.v1.user_api import router as users_router
from core.cors import setup_cors
from core.config import settings
from db.database import engine, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Se ejecuta al iniciar
    print("Iniciando base de datos...")
    if not settings.USE_ALEMBIC:
        create_db_and_tables()
    yield
    # Shutdown: Se ejecuta al cerrar (aquí podrías cerrar conexiones)
    print("Cerrando aplicación...")

# Crear la app con lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION or '',
    version=settings.PROJECT_VERSION,
    lifespan=lifespan  # <-- Aquí está el cambio clave
)

# Configurar CORS desde core
setup_cors(app, settings.CORS_ORIGINS)

# Incluir routers
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
