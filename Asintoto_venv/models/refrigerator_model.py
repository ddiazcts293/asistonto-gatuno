# models.py
from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from models.user_model import User

class Refrigerador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str

    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional[User] = Relationship(back_populates='refrigerators')

    # Un refrigerador tiene muchos alimentos (1:N DIRECTO)
    # cascade='all, delete-orphan' asegura que si borro el refri, se borran sus alimentos
    foods: List['Food'] = Relationship(
        back_populates='refrigerator',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
