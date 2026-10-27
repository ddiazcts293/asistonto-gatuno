import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Datos necesarios para crear un usuario"""
    name: str = Field(..., min_length=2, max_length=120, description='Nombre completo')
    username: str = Field(..., min_length=3, max_length=60, description='Nombre de usuario')
    email: EmailStr = Field(..., max_length=60, description='Correo electrónico')
    password: str = Field(..., min_length=8, description='Contraseña (mínimo 8 caracteres)')
    phone_number: Optional[str] = Field(None, min_length=10, max_length=16, description='Número de teléfono en formato XXX-XXX-XXXX o +XX-XXX-XXX-XXXX')

class UserUpdate(BaseModel):
    """Datos opcionales para actualizar un usuario"""
    name: Optional[str] = Field(None, min_length=2, max_length=120, description='Nombre completo')
    username: Optional[str] = Field(None, min_length=3, max_length=60, description='Nombre de usuario')
    email: Optional[EmailStr] = Field(None, max_length=60, description='Correo electrónico')
    password: Optional[str] = Field(None, min_length=8, description='Contraseña (mínimo 8 caracteres)')
    is_active: Optional[bool] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=16,  description='Número de teléfono en formato XXX-XXX-XXXX o +XX-XXX-XXX-XXXX')

class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    username: str
    email: str
    phone_number: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
