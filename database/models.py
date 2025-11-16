"""
SQLAlchemy ORM Models for MathCopain v6.3
Phase 7: PostgreSQL Migration

Defines 7 tables:
1. users - User accounts
2. exercise_responses - Exercise history
3. skill_profiles - Skill competencies
4. parent_accounts - Parent accounts
5. parent_child_links - Parent-child relationships
6. analytics_events - Event tracking
7. ml_models - ML model metadata
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text, CheckConstraint, Index, JSONB
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """
    User accounts for students

    Stores student profiles with authentication and learning preferences
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    pin_hash = Column(String(255), nullable=False)
    learning_style = Column(String(20))  # visual, auditory, kinesthetic, logical, narrative
    grade_level = Column(String(10))  # CE1, CE2, CM1, CM2
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    exercise_responses = relationship(
        "ExerciseResponse",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    skill_profiles = relationship(
        "SkillProfile",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    analytics_events = relationship(
        "AnalyticsEvent",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    parent_links = relationship(
        "ParentChildLink",
        back_populates="child",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', grade={self.grade_level})>"


class ExerciseResponse(Base):
    """
    Historical record of all exercise attempts

    Stores complete exercise history for analytics and ML training
    """
    __tablename__ = 'exercise_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    exercise_id = Column(String(100), nullable=False)
    skill_domain = Column(String(50), nullable=False, index=True)
    difficulty_level = Column(
        Integer,
        CheckConstraint('difficulty_level BETWEEN 1 AND 5'),
        nullable=False
    )
    question = Column(Text)
    user_response = Column(Text)
    expected_answer = Column(Text)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer)
    strategy_used = Column(String(100))  # mental, fingers, drawing, formula
    error_type = Column(String(50))  # conceptual, procedural, calculation
    feedback_given = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="exercise_responses")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_skill', 'user_id', 'skill_domain'),
        Index('idx_user_created_desc', 'user_id', 'created_at'),
    )

    def __repr__(self):
        status = "✓" if self.is_correct else "✗"
        return f"<ExerciseResponse(id={self.id}, user={self.user_id}, {status} {self.skill_domain} D{self.difficulty_level})>"


class SkillProfile(Base):
    """
    Skill proficiency profiles per user per domain

    Tracks mastery level for each mathematical domain
    """
    __tablename__ = 'skill_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_domain = Column(String(50), nullable=False)
    proficiency_level = Column(
        Float,
        CheckConstraint('proficiency_level BETWEEN 0 AND 1'),
        nullable=False,
        default=0.0
    )
    exercises_completed = Column(Integer, default=0)
    success_rate = Column(Float)
    last_practiced = Column(DateTime)
    mastery_date = Column(DateTime)  # When proficiency reached 0.8+

    # Relationships
    user = relationship("User", back_populates="skill_profiles")

    # Constraints
    __table_args__ = (
        Index('idx_user_profile', 'user_id'),
        Index('idx_domain_profile', 'skill_domain'),
        # Ensure one profile per user per domain
        CheckConstraint('user_id IS NOT NULL AND skill_domain IS NOT NULL'),
    )

    def __repr__(self):
        mastery = "🌟" if self.proficiency_level >= 0.8 else ""
        return f"<SkillProfile(user={self.user_id}, {self.skill_domain}: {self.proficiency_level:.0%} {mastery})>"


class ParentAccount(Base):
    """
    Parent accounts for monitoring children

    Allows parents to track their children's progress
    """
    __tablename__ = 'parent_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    child_links = relationship(
        "ParentChildLink",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ParentAccount(id={self.id}, username='{self.username}')>"


class ParentChildLink(Base):
    """
    Links between parent and child accounts

    Manages permissions for parent access to child data
    """
    __tablename__ = 'parent_child_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('parent_accounts.id', ondelete='CASCADE'), nullable=False)
    child_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    permission_level = Column(String(20), default='view')  # view, edit, admin
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    parent = relationship("ParentAccount", back_populates="child_links")
    child = relationship("User", back_populates="parent_links")

    # Indexes
    __table_args__ = (
        Index('idx_parent_link', 'parent_id'),
        Index('idx_child_link', 'child_id'),
    )

    def __repr__(self):
        return f"<ParentChildLink(parent={self.parent_id}, child={self.child_id}, perm={self.permission_level})>"


class AnalyticsEvent(Base):
    """
    Analytics event tracking

    Stores all user interactions for behavioral analysis
    """
    __tablename__ = 'analytics_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_type = Column(String(50), nullable=False)  # login, exercise_start, exercise_complete, etc.
    event_data = Column(JSONB)  # Flexible JSON storage
    session_id = Column(String(100), index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="analytics_events")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_event_type', 'user_id', 'event_type'),
        Index('idx_session_events', 'session_id'),
    )

    def __repr__(self):
        return f"<AnalyticsEvent(id={self.id}, user={self.user_id}, type='{self.event_type}')>"


class MLModel(Base):
    """
    ML model metadata and versioning

    Tracks trained models, versions, and performance metrics
    """
    __tablename__ = 'ml_models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)  # DifficultyOptimizer, PerformancePredictor
    model_version = Column(String(20), nullable=False)  # v1.0, v1.1, etc.
    model_type = Column(String(50))  # xgboost, random_forest, lstm
    training_date = Column(DateTime)
    accuracy_metrics = Column(JSONB)  # {mae: 0.42, r2: 0.78, ...}
    model_path = Column(String(255))  # File path to .pkl
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_model_active', 'model_name', 'is_active'),
    )

    def __repr__(self):
        active = "✓" if self.is_active else "✗"
        return f"<MLModel({active} {self.model_name} {self.model_version})>"
