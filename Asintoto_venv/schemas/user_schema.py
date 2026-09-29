from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# '...' es requerido para especificar un campo obligatorio

class UserCreate(BaseModel):
    """Datos necesarios para crear un usuario"""
    username: str = Field(..., min_length=3, max_length=50, description='Nombre de usuario')
    email: EmailStr = Field(..., description='Correo electrónico')
    password: str = Field(..., min_length=8, description='Contraseña (mínimo 8 caracteres)')
    date_of_birth: datetime = Field(..., description='Fecha de nacimiento')
    phone_number: str = Field(..., min_length=10, max_length=16, description='Número de teléfono en formato XXX-XXX-XXXX o +XX-XXX-XXX-XXXX')
    address: Optional[str] = Field(None, max_length=160, description='Dirección completa')

class UserUpdate(BaseModel):
    """Datos opcionales para actualizar un usuario"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=16)
    address: Optional[str] = Field(None, max_length=160)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    date_of_birth: datetime
    phone_number: str
    address: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Permite convertir modelos SQLModel a Pydantic
