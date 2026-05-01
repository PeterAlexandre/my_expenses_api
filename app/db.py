from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def init_db() -> None:
    # Importa os modelos para registrar metadata antes do create_all
    from app.models import (  # noqa: F401, PLC0415
        transaction,
        transaction_category,
        user,
    )
    from app.models.base import Base  # noqa: PLC0415

    Base.metadata.create_all(bind=engine)
