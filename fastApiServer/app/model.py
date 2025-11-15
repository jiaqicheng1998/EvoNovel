import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine


class ClickCount(SQLModel, table=True):
    user_agent_ip: str = Field(primary_key=True)
    click_count: int = Field(default=0)


raw_database_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")
if raw_database_url.startswith("postgresql://"):
    raw_database_url = raw_database_url.replace("postgresql://", "postgresql+psycopg://", 1)

DATABASE_URL = raw_database_url

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

