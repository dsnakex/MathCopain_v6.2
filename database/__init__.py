"""
Database package for MathCopain Phase 7
PostgreSQL integration with SQLAlchemy ORM
"""

from database.models import (
    User,
    ExerciseResponse,
    SkillProfile,
    ParentAccount,
    ParentChildLink,
    AnalyticsEvent,
    MLModel,
    Base
)

from database.connection import get_engine, get_session

__all__ = [
    'User',
    'ExerciseResponse',
    'SkillProfile',
    'ParentAccount',
    'ParentChildLink',
    'AnalyticsEvent',
    'MLModel',
    'Base',
    'get_engine',
    'get_session'
]
