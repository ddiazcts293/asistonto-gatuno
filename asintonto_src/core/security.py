from passlib.context import CryptContext
from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

# Configuración para Argon2
pwd_context = CryptContext(
    schemes=[settings.HASHING_ALGORITHM],
    deprecated='auto',
    argon2__time_cost=2,
    argon2__memory_cost=10240,
    argon2__parallelism=2
)

def get_password_hash(password: str) -> str:
    """Hashea la contraseña usando Argon2"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

# Funciones JWT

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

    return encoded_jwt
