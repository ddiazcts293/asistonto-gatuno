from collections.abc import Generator

from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

connect_args = {}

if 'sqlite' in settings.DATABASE_URL:
    connect_args = { 'check_same_thread': False }

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
