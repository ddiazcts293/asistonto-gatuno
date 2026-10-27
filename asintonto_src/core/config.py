from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Datos generales
    PROJECT_NAME: str = 'asistonto_gatuno_v1'
    PROJECT_DESCRIPTION: str | None = None
    PROJECT_VERSION: str = "1.0.0"

    # Configuración de base de datos
    DATABASE_URL: str

    # Configuración de autenticación JWT
    SECRET_KEY: str
    HASHING_ALGORITHM: str = 'argon2'
    TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USE_ALEMBIC: bool = True
    CORS_ORIGINS: list[str] = [
        'http://localhost:3000',
        'http://localhost:8000'
    ]

    # Configuración de Pydantic v2
    model_config = {
        'env_file': '.env',
        'extra': 'ignore'
    }

settings = Settings()
