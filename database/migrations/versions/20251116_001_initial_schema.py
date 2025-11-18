"""Initial schema for MathCopain Phase 7

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-11-16 18:00:00

Creates all 7 core tables:
1. users
2. exercise_responses
3. skill_profiles
4. parent_accounts
5. parent_child_links
6. analytics_events
7. ml_models
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('pin_hash', sa.String(length=255), nullable=False),
        sa.Column('learning_style', sa.String(length=20), nullable=True),
        sa.Column('grade_level', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_username', 'users', ['username'], unique=True)
    op.create_index('idx_user_active', 'users', ['is_active'], unique=False)

    # Create parent_accounts table
    op.create_table(
        'parent_accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_parent_username', 'parent_accounts', ['username'], unique=True)
    op.create_index('idx_parent_email', 'parent_accounts', ['email'], unique=True)

    # Create exercise_responses table
    op.create_table(
        'exercise_responses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exercise_id', sa.String(length=100), nullable=False),
        sa.Column('skill_domain', sa.String(length=50), nullable=False),
        sa.Column('difficulty_level', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=True),
        sa.Column('user_response', sa.Text(), nullable=True),
        sa.Column('expected_answer', sa.Text(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('time_taken_seconds', sa.Integer(), nullable=True),
        sa.Column('strategy_used', sa.String(length=100), nullable=True),
        sa.Column('error_type', sa.String(length=50), nullable=True),
        sa.Column('feedback_given', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('difficulty_level BETWEEN 1 AND 5', name='check_difficulty_level'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_skill', 'exercise_responses', ['user_id', 'skill_domain'], unique=False)
    op.create_index('idx_user_created_desc', 'exercise_responses', ['user_id', 'created_at'], unique=False)
    op.create_index('idx_skill_domain', 'exercise_responses', ['skill_domain'], unique=False)

    # Create skill_profiles table
    op.create_table(
        'skill_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('skill_domain', sa.String(length=50), nullable=False),
        sa.Column('proficiency_level', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('exercises_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('success_rate', sa.Float(), nullable=True),
        sa.Column('last_practiced', sa.DateTime(), nullable=True),
        sa.Column('mastery_date', sa.DateTime(), nullable=True),
        sa.CheckConstraint('proficiency_level BETWEEN 0 AND 1', name='check_proficiency_level'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_profile', 'skill_profiles', ['user_id'], unique=False)
    op.create_index('idx_domain_profile', 'skill_profiles', ['skill_domain'], unique=False)
    # Ensure one profile per user per domain
    op.create_index('idx_user_domain_unique', 'skill_profiles', ['user_id', 'skill_domain'], unique=True)

    # Create parent_child_links table
    op.create_table(
        'parent_child_links',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=False),
        sa.Column('child_id', sa.Integer(), nullable=False),
        sa.Column('permission_level', sa.String(length=20), nullable=True, server_default='view'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['parent_accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['child_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_parent_link', 'parent_child_links', ['parent_id'], unique=False)
    op.create_index('idx_child_link', 'parent_child_links', ['child_id'], unique=False)
    op.create_index('idx_parent_child_unique', 'parent_child_links', ['parent_id', 'child_id'], unique=True)

    # Create analytics_events table
    op.create_table(
        'analytics_events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_data', JSONB, nullable=True),
        sa.Column('session_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_event_type', 'analytics_events', ['user_id', 'event_type'], unique=False)
    op.create_index('idx_session_events', 'analytics_events', ['session_id'], unique=False)
    op.create_index('idx_event_created', 'analytics_events', ['created_at'], unique=False)

    # Create ml_models table
    op.create_table(
        'ml_models',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('model_version', sa.String(length=20), nullable=False),
        sa.Column('model_type', sa.String(length=50), nullable=True),
        sa.Column('training_date', sa.DateTime(), nullable=True),
        sa.Column('accuracy_metrics', JSONB, nullable=True),
        sa.Column('model_path', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_model_active', 'ml_models', ['model_name', 'is_active'], unique=False)

    print("✓ All tables created successfully")


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('ml_models')
    op.drop_table('analytics_events')
    op.drop_table('parent_child_links')
    op.drop_table('skill_profiles')
    op.drop_table('exercise_responses')
    op.drop_table('parent_accounts')
    op.drop_table('users')

    print("✓ All tables dropped successfully")
