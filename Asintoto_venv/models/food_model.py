from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from models.user_model import User
from models.refrigerator_model import Refrigerador

class Food(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # ej: 'Leche Alpura'
    type: str = Field(index=True)    # ej: 'Lácteo'
    quantity: int = Field(ge=0)
    best_before: date = Field(index=True)

    # CLAVE FORÁNEA DIRECTA: Este alimento pertenece a UN solo refrigerador
    refrigerator_id: Optional[int] = Field(default=None, foreign_key='refrigerator.id')

    # Relación inversa
    refrigerator: Optional[Refrigerador] = Relationship(back_populates='foods')
