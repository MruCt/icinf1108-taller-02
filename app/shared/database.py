
import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("La variable DATABASE_URL no está configurada.")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


@contextmanager
def session_scope(session: Session | None = None) -> Iterator[Session]:
    if session is not None:
        # La transacción pertenece al servicio que creó esta sesión.
        yield session
    else:
        # Para operaciones independientes, gestionamos la transacción aquí.
        with SessionLocal.begin() as new_session:
            yield new_session
