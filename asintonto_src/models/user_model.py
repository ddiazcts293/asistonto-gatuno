from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True)
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    phone_number: str = Field(min_length=10, max_length=16, unique=True)
    address: Optional[str] = Field(default=None, max_length=160)
    date_of_birth: datetime = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = 'users'
