from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración de base de datos
    DATABASE_URL: str

    # Configuración de autenticación JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de Pydantic v2
    model_config = {
        'env_file': '.env',
        'extra': 'ignore'
    }

settings = Settings()
