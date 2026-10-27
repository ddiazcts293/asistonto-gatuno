import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import timedelta

# Importaciones de proyecto
from db.database import get_session
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from schemas.token_schema import Token, TokenData
from core.security import get_password_hash, verify_password, create_access_token
from core.config import settings
from api.v1.dependencies import get_current_user

router = APIRouter()

# -----------------
# Registrar usuario
# -----------------
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> User:
    """
    Crea un nuevo usuario en la base de datos.
    """

    # Verificar si el email ya existe
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Verificar si el username ya existe
    statement = select(User).where(User.username == user_data.username)
    existing_username = session.exec(statement).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )

    # Hashear la contraseña
    hashed_password = get_password_hash(user_data.password)

    # Crear el usuario (en producción, hashear la contraseña con bcrypt)
    db_user = User(
        username=user_data.username,
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        hashed_password=hashed_password,
        is_active=True
    )

    session.add(db_user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El nombre de usuario o correo electrónico ya está registrado.'
        ) from None

    session.refresh(db_user)
    return db_user

# --------------------------
# Obtener todos los usuarios
# --------------------------
@router.get("/", response_model=List[UserResponse])
def get_users(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
) -> list[User]:
    """
    Obtiene todos los usuarios registrados.
    """

    users = session.exec(select(User)).all()
    return list(users)

# ----------------------
# Obtener usuario por ID
# ----------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
) -> User:
    """
    Obtiene un usuario específico por su ID.
    """

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    return user

# ------------------
# Actualizar usuario
# ------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
) -> User:
    """
    Actualiza los datos de un usuario existente.
    """

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    # Actualizar solo los campos que vienen en el request
    # 'Truco de magia' para permitir actualizaciones parciales (cuando el
    # cliente solo quiere cambiar uno o dos campos, no todo el registro).
    update_data = user_update.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Los campos enviados no pueden ser null.",
        )

    if 'username' in update_data or 'email' in update_data:
        statement = select(User).where(User.id != user_id,
            (User.username == update_data.get("username", db_user.username)) |
            (User.email == update_data.get("email", db_user.email)),
        )
        duplicate = session.exec(statement).first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario o correo ya está registrado.",
            )

    # Verificar si se está actualizando la contraseña
    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    session.add(db_user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o correo ya está registrado.",
        ) from None

    session.refresh(db_user)
    return db_user

# ----------------
# Eliminar usuario
# ----------------
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    """
    Elimina un usuario de la base de datos.
    """

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Usuario con ID {user_id} no encontrado'
        )

    session.delete(db_user)
    session.commit()

    return None  # 204 No Content no devuelve nada

# --------------
# Iniciar sesión
# --------------
@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
) -> Token:
    """
    Obtiene un token de acceso JWT validando el usuario y la contraseña.
    """

    # 1. Busca el usuario en la DB por su nombre
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    # 2. Valida que el usuario exista y que la contraseña coincida con el hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # 3. Genera el token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username },
        expires_delta=access_token_expires
    )

    # 4. Retoma el token en el formato estándar OAuth2
    return Token(access_token= access_token)
