"""Add teacher and classroom tables for Phase 8

Revision ID: 002_teacher_classroom
Revises: 001_initial_schema
Create Date: 2025-11-16 19:00:00

Creates 7 new tables for institutional deployment:
1. teacher_accounts
2. classrooms
3. classroom_enrollments
4. assignments
5. assignment_completions
6. curriculum_competencies
7. student_competency_progress
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '002_teacher_classroom'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create teacher_accounts table
    op.create_table(
        'teacher_accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('school_name', sa.String(length=100), nullable=True),
        sa.Column('grade_levels', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_teacher_username', 'teacher_accounts', ['username'], unique=True)
    op.create_index('idx_teacher_email', 'teacher_accounts', ['email'], unique=True)
    op.create_index('idx_teacher_active', 'teacher_accounts', ['is_active'], unique=False)

    # Create classrooms table
    op.create_table(
        'classrooms',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('grade_level', sa.String(length=10), nullable=False),
        sa.Column('school_year', sa.String(length=10), nullable=True),
        sa.Column('max_students', sa.Integer(), nullable=True, server_default='30'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['teacher_id'], ['teacher_accounts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_classroom_teacher', 'classrooms', ['teacher_id'], unique=False)
    op.create_index('idx_classroom_active', 'classrooms', ['is_active'], unique=False)

    # Create classroom_enrollments table
    op.create_table(
        'classroom_enrollments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('classroom_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('enrolled_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='active'),
        sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_enrollment_classroom', 'classroom_enrollments', ['classroom_id'], unique=False)
    op.create_index('idx_enrollment_student', 'classroom_enrollments', ['student_id'], unique=False)
    op.create_index('idx_enrollment_unique', 'classroom_enrollments', ['classroom_id', 'student_id'], unique=True)

    # Create assignments table
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('classroom_id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('skill_domains', JSONB, nullable=True),
        sa.Column('difficulty_levels', JSONB, nullable=True),
        sa.Column('exercise_count', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=True, server_default='false'),
        sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['teacher_id'], ['teacher_accounts.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_assignment_classroom', 'assignments', ['classroom_id'], unique=False)
    op.create_index('idx_assignment_due', 'assignments', ['due_date'], unique=False)

    # Create assignment_completions table
    op.create_table(
        'assignment_completions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('exercises_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('exercises_total', sa.Integer(), nullable=True),
        sa.Column('success_rate', sa.Float(), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='in_progress'),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_completion_assignment', 'assignment_completions', ['assignment_id'], unique=False)
    op.create_index('idx_completion_student', 'assignment_completions', ['student_id'], unique=False)
    op.create_index('idx_completion_unique', 'assignment_completions', ['assignment_id', 'student_id'], unique=True)

    # Create curriculum_competencies table
    op.create_table(
        'curriculum_competencies',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('grade_level', sa.String(length=10), nullable=False),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('subdomain', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('skill_domains', JSONB, nullable=True),
        sa.Column('examples', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_competency_code', 'curriculum_competencies', ['code'], unique=True)
    op.create_index('idx_competency_grade', 'curriculum_competencies', ['grade_level'], unique=False)
    op.create_index('idx_competency_domain', 'curriculum_competencies', ['domain'], unique=False)

    # Create student_competency_progress table
    op.create_table(
        'student_competency_progress',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('competency_id', sa.Integer(), nullable=False),
        sa.Column('proficiency_level', sa.Float(), nullable=True),
        sa.Column('exercises_done', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('last_practiced', sa.DateTime(), nullable=True),
        sa.Column('mastery_achieved', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('mastery_date', sa.DateTime(), nullable=True),
        sa.CheckConstraint('proficiency_level BETWEEN 0 AND 1', name='check_competency_proficiency'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['competency_id'], ['curriculum_competencies.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_progress_student', 'student_competency_progress', ['student_id'], unique=False)
    op.create_index('idx_progress_competency', 'student_competency_progress', ['competency_id'], unique=False)
    op.create_index('idx_progress_unique', 'student_competency_progress', ['student_id', 'competency_id'], unique=True)

    print("✓ All Phase 8 tables created successfully")


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('student_competency_progress')
    op.drop_table('curriculum_competencies')
    op.drop_table('assignment_completions')
    op.drop_table('assignments')
    op.drop_table('classroom_enrollments')
    op.drop_table('classrooms')
    op.drop_table('teacher_accounts')

    print("✓ All Phase 8 tables dropped successfully")
