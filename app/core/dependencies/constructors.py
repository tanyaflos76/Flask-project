from typing import Any, AsyncGenerator, Generator

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import AppConfig


def db_engine(database_url: str) -> Engine:
    return create_engine(database_url, isolation_level="SERIALIZABLE")


def db_session_maker(
    engine: Engine | str,
) -> Generator[sessionmaker[Any], None, None]:
    engine = engine if isinstance(engine, Engine) else db_engine(engine)
    maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[call-overload]
    yield maker
    maker.close_all()


async def db_session(maker: sessionmaker[Any]) -> AsyncGenerator[AsyncSession, None]:
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


def db_session_autocommit(
    maker: sessionmaker[Any],
) -> Generator[Session, None, None]:
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()


def app_config() -> AppConfig:
    return AppConfig.from_env()
