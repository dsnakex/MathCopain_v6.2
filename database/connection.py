"""
Database connection management for MathCopain
Handles PostgreSQL connections with pooling
"""

import os
from typing import Optional
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mathcopain')
DB_USER = os.getenv('DB_USER', 'mathcopain_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mathcopain_password')

# Connection pool configuration
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '20'))
POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '3600'))

# Global engine and session factory
_engine: Optional[Engine] = None
_SessionFactory: Optional[sessionmaker] = None


def get_database_url() -> str:
    """
    Construct PostgreSQL database URL

    Returns:
        str: Database connection URL
    """
    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def create_db_engine(echo: bool = False) -> Engine:
    """
    Create SQLAlchemy engine with connection pooling

    Args:
        echo: If True, log all SQL queries (for debugging)

    Returns:
        Engine: SQLAlchemy engine instance
    """
    database_url = get_database_url()

    engine = create_engine(
        database_url,
        echo=echo,
        poolclass=QueuePool,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=True,  # Verify connections before using
    )

    # Enable foreign key constraints for PostgreSQL
    @event.listens_for(engine, "connect")
    def set_postgres_options(dbapi_conn, connection_record):
        """Set PostgreSQL connection options"""
        cursor = dbapi_conn.cursor()
        cursor.execute("SET timezone='UTC'")
        cursor.close()

    return engine


def get_engine(echo: bool = False) -> Engine:
    """
    Get or create global database engine (singleton pattern)

    Args:
        echo: If True, log SQL queries

    Returns:
        Engine: Global engine instance
    """
    global _engine

    if _engine is None:
        _engine = create_db_engine(echo=echo)

    return _engine


def get_session_factory() -> sessionmaker:
    """
    Get or create global session factory

    Returns:
        sessionmaker: Session factory
    """
    global _SessionFactory

    if _SessionFactory is None:
        engine = get_engine()
        _SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)

    return _SessionFactory


def get_session() -> Session:
    """
    Create a new database session

    Returns:
        Session: SQLAlchemy session

    Usage:
        with get_session() as session:
            # Use session here
            user = session.query(User).first()
    """
    SessionFactory = get_session_factory()
    return SessionFactory()


def init_database(drop_all: bool = False, echo: bool = False):
    """
    Initialize database tables

    Args:
        drop_all: If True, drop all tables first (USE WITH CAUTION!)
        echo: If True, log SQL queries

    Warning:
        Setting drop_all=True will DELETE ALL DATA!
    """
    from database.models import Base

    engine = get_engine(echo=echo)

    if drop_all:
        print("⚠️  Dropping all tables...")
        Base.metadata.drop_all(engine)

    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("✓ Database tables created successfully")


def close_connections():
    """
    Close all database connections

    Call this when shutting down the application
    """
    global _engine, _SessionFactory

    if _engine:
        _engine.dispose()
        _engine = None

    _SessionFactory = None
    print("✓ Database connections closed")


# Context manager for database sessions
class DatabaseSession:
    """
    Context manager for database sessions with automatic commit/rollback

    Usage:
        with DatabaseSession() as session:
            user = User(username='test')
            session.add(user)
            # Automatically commits on success, rolls back on error
    """

    def __init__(self):
        self.session: Optional[Session] = None

    def __enter__(self) -> Session:
        self.session = get_session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Error occurred, rollback
            self.session.rollback()
            print(f"❌ Transaction rolled back: {exc_val}")
        else:
            # Success, commit
            self.session.commit()

        self.session.close()


def test_connection() -> bool:
    """
    Test database connection

    Returns:
        bool: True if connection successful
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    print("Testing database connection...")
    test_connection()
