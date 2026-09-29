from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

# Importaciones del proyecto
from db.database import get_session
from core.config import settings
from models.user_model import User

# tokenUrl debe coincidir con la ruta completa del endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/user/token')

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """Dependencia para validar el token JWT y retornar el usuario autenticado"""

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Cannot validate user credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Decodifica el token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub') if payload is not None else None

        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependencia para verificar que el usuario esté activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is inactive'
        )

    return current_user
