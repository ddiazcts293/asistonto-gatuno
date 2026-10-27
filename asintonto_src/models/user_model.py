import uuid
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[uuid.UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(index=True, min_length=2, max_length=120)
    username: str = Field(index=True, unique=True, min_length=3, max_length=60)
    email: str = Field(index=True, unique=True, max_length=60)
    phone_number: Optional[str] = Field(default=None, min_length=10, max_length=16, unique=True)
    hashed_password: str = Field(max_length=256)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
