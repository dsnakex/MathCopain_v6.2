"""
Database session utilities and helpers
"""

from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy.orm import Session

from database.connection import get_session


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations

    Usage:
        with session_scope() as session:
            user = User(username='test')
            session.add(user)
            # Automatically commits on exit, rolls back on error

    Yields:
        Session: Database session
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def execute_in_session(func):
    """
    Decorator to automatically manage database sessions

    Usage:
        @execute_in_session
        def create_user(session, username):
            user = User(username=username)
            session.add(user)
            return user

    Args:
        func: Function that takes session as first argument

    Returns:
        Wrapped function with automatic session management
    """
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            return func(session, *args, **kwargs)
    return wrapper
