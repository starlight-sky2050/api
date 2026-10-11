"""資料庫連線管理。

這個模組提供 FastAPI dependency，讓每個 API request 都能取得一個
PostgreSQL connection，並在 request 結束時自動關閉它。
"""

import os
from collections.abc import Generator
from functools import lru_cache

import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# 從專案根目錄的 .env 載入本機開發設定。
load_dotenv()


class Base(DeclarativeBase):
    """SQLAlchemy ORM model base."""


@lru_cache
def _get_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return create_engine(database_url)


@lru_cache
def _get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=_get_engine(), autoflush=False, expire_on_commit=False)


def create_db_tables() -> None:
    """Create the registered ORM tables if they do not already exist."""

    from app.models.asset import Asset
    from app.models.permission import Permission
    from app.models.tag import Tag
    from app.models.team import Team
    from app.models.user import User

    Base.metadata.create_all(
        bind=_get_engine(),
        tables=[
            Asset.__table__,
            Team.__table__,
            User.__table__,
            Permission.__table__,
            Tag.__table__,
        ],
    )


def get_db_session() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session for one API request."""

    session = _get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def get_db_connection() -> Generator[psycopg.Connection, None, None]:
    """提供一個 request 期間使用的 PostgreSQL connection。

    使用 yield 是因為 FastAPI dependency 可以在 yield 前準備資源，
    讓 endpoint 使用；endpoint 完成後，再執行 finally 裡的清理工作。
    """

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # 提前回報設定錯誤，比讓 psycopg 用空值連線更容易理解原因。
        raise RuntimeError("DATABASE_URL is not configured")

    connection = psycopg.connect(database_url)
    try:
        yield connection
    finally:
        # 不論查詢成功或發生例外，都要關閉連線，避免 connection leak。
        connection.close()