"""
SQLAlchemy ORM Models for MathCopain v6.4
Phase 7 + Phase 8: PostgreSQL Migration + Institutional Deployment

Phase 7 (7 tables):
1. users - User accounts
2. exercise_responses - Exercise history
3. skill_profiles - Skill competencies
4. parent_accounts - Parent accounts
5. parent_child_links - Parent-child relationships
6. analytics_events - Event tracking
7. ml_models - ML model metadata

Phase 8 (7 tables):
8. teacher_accounts - Teacher accounts
9. classrooms - Classroom management
10. classroom_enrollments - Student-classroom links
11. assignments - Homework assignments
12. assignment_completions - Assignment progress tracking
13. curriculum_competencies - French National Curriculum
14. student_competency_progress - Student progress on competencies
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey,
    Integer, String, Text, CheckConstraint, Index
)
from sqlalchemy.dialects.postgresql import JSONB
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


# ============================================================================
# PHASE 8 MODELS - Institutional Deployment
# ============================================================================


class TeacherAccount(Base):
    """
    Teacher accounts for classroom management

    Stores teacher profiles with authentication and school information
    """
    __tablename__ = 'teacher_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    school_name = Column(String(100))
    grade_levels = Column(String(50))  # JSON array: ["CE1", "CE2"]
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    classrooms = relationship(
        "Classroom",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )
    assignments = relationship("Assignment", back_populates="teacher")

    def __repr__(self):
        return f"<TeacherAccount(id={self.id}, name='{self.first_name} {self.last_name}')>"


class Classroom(Base):
    """
    Classrooms managed by teachers

    Organizes students into classes with grade level and school year
    """
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey('teacher_accounts.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)  # "CE2 - Classe A"
    grade_level = Column(String(10), nullable=False)  # "CE2"
    school_year = Column(String(10))  # "2025-2026"
    max_students = Column(Integer, default=30)
    description = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    teacher = relationship("TeacherAccount", back_populates="classrooms")
    enrollments = relationship(
        "ClassroomEnrollment",
        back_populates="classroom",
        cascade="all, delete-orphan"
    )
    assignments = relationship(
        "Assignment",
        back_populates="classroom",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_classroom_teacher', 'teacher_id'),
    )

    def __repr__(self):
        return f"<Classroom(id={self.id}, name='{self.name}', students={len(self.enrollments)})>"


class ClassroomEnrollment(Base):
    """
    Student enrollment in classrooms

    Links students to classrooms with enrollment status
    """
    __tablename__ = 'classroom_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_id = Column(Integer, ForeignKey('classrooms.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    enrolled_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(20), default='active')  # active, completed, withdrawn

    # Relationships
    classroom = relationship("Classroom", back_populates="enrollments")
    student = relationship("User")

    __table_args__ = (
        Index('idx_enrollment_classroom', 'classroom_id'),
        Index('idx_enrollment_student', 'student_id'),
    )

    def __repr__(self):
        return f"<ClassroomEnrollment(classroom={self.classroom_id}, student={self.student_id})>"


class Assignment(Base):
    """
    Homework/exercise assignments for classrooms

    Teachers create assignments with specific domains, difficulty, and deadlines
    """
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_id = Column(Integer, ForeignKey('classrooms.id', ondelete='CASCADE'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher_accounts.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    skill_domains = Column(JSONB)  # ["addition", "multiplication"]
    difficulty_levels = Column(JSONB)  # [2, 3, 4]
    exercise_count = Column(Integer, default=10)
    due_date = Column(DateTime, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_published = Column(Boolean, default=False)

    # Relationships
    classroom = relationship("Classroom", back_populates="assignments")
    teacher = relationship("TeacherAccount", back_populates="assignments")
    completions = relationship(
        "AssignmentCompletion",
        back_populates="assignment",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_assignment_classroom', 'classroom_id'),
    )

    def __repr__(self):
        status = "✓" if self.is_published else "📝"
        return f"<Assignment({status} '{self.title}', due={self.due_date})>"


class AssignmentCompletion(Base):
    """
    Tracks student completion of assignments

    Records progress, success rate, and completion status
    """
    __tablename__ = 'assignment_completions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    exercises_completed = Column(Integer, default=0)
    exercises_total = Column(Integer)
    success_rate = Column(Float)
    time_spent_seconds = Column(Integer)
    completed_at = Column(DateTime)
    status = Column(String(20), default='in_progress')  # in_progress, completed, overdue

    # Relationships
    assignment = relationship("Assignment", back_populates="completions")
    student = relationship("User")

    __table_args__ = (
        Index('idx_completion_assignment', 'assignment_id'),
        Index('idx_completion_student', 'student_id'),
    )

    def __repr__(self):
        progress = f"{self.exercises_completed}/{self.exercises_total}" if self.exercises_total else "0/?"
        return f"<AssignmentCompletion(assignment={self.assignment_id}, student={self.student_id}, {progress})>"


class CurriculumCompetency(Base):
    """
    French National Curriculum competencies

    Maps official Education Nationale competencies to our skill domains
    """
    __tablename__ = 'curriculum_competencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # "NUM.CE2.01"
    grade_level = Column(String(10), nullable=False, index=True)  # "CE2"
    domain = Column(String(50), nullable=False, index=True)  # "Nombres et calculs"
    subdomain = Column(String(100))  # "Addition et soustraction"
    description = Column(Text)
    skill_domains = Column(JSONB)  # Mapping to our domains
    examples = Column(Text)

    # Relationships
    student_progress = relationship(
        "StudentCompetencyProgress",
        back_populates="competency",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<CurriculumCompetency({self.code}: {self.domain})>"


class StudentCompetencyProgress(Base):
    """
    Student progress on curriculum competencies

    Tracks proficiency level and mastery for each EN competency
    """
    __tablename__ = 'student_competency_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    competency_id = Column(Integer, ForeignKey('curriculum_competencies.id'), nullable=False)
    proficiency_level = Column(
        Float,
        CheckConstraint('proficiency_level BETWEEN 0 AND 1')
    )
    exercises_done = Column(Integer, default=0)
    last_practiced = Column(DateTime)
    mastery_achieved = Column(Boolean, default=False)
    mastery_date = Column(DateTime)

    # Relationships
    student = relationship("User")
    competency = relationship("CurriculumCompetency", back_populates="student_progress")

    __table_args__ = (
        Index('idx_progress_student', 'student_id'),
        Index('idx_progress_competency', 'competency_id'),
    )

    def __repr__(self):
        mastery = "🌟" if self.mastery_achieved else ""
        return f"<StudentCompetencyProgress(student={self.student_id}, {self.proficiency_level:.0%} {mastery})>"
