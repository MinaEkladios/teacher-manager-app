"""Initial migration: create core schema

Revision ID: 001
Revises: 
Create Date: 2026-03-12 00:00:00.000000

Creates:
- schools table
- users table (with school FK)
- students table (with school FK)
- classes table (with school + teacher FK)
- attendance table (with student + class + user FK)
- audit_logs table (with school + user FK + entity refs)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade to revision 001: create initial schema."""
    # Create schools table
    op.create_table(
        'schools',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('timezone', sa.String(50), server_default='UTC'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schools_name'), 'schools', ['name'], unique=False)

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('school_id', sa.String(36), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', 'school_id', name='uq_user_email_school')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_school_id'), 'users', ['school_id'], unique=False)

    # Create students table
    op.create_table(
        'students',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('school_id', sa.String(36), nullable=False),
        sa.Column('student_id', sa.String(50), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('parent_email', sa.String(255), nullable=True),
        sa.Column('parent_phone', sa.String(20), nullable=True),
        sa.Column('enrollment_date', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'school_id', name='uq_student_id_school')
    )
    op.create_index(op.f('ix_students_is_active'), 'students', ['is_active'], unique=False)
    op.create_index(op.f('ix_students_school_id'), 'students', ['school_id'], unique=False)

    # Create classes table
    op.create_table(
        'classes',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('school_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('teacher_id', sa.String(36), nullable=False),
        sa.Column('grade_level', sa.String(50), nullable=True),
        sa.Column('room_number', sa.String(50), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
        sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classes_code'), 'classes', ['code'], unique=False)
    op.create_index(op.f('ix_classes_is_active'), 'classes', ['is_active'], unique=False)
    op.create_index(op.f('ix_classes_school_id'), 'classes', ['school_id'], unique=False)

    # Create attendance table
    op.create_table(
        'attendance',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('student_id', sa.String(36), nullable=False),
        sa.Column('class_id', sa.String(36), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('marked_by_user_id', sa.String(36), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
        sa.ForeignKeyConstraint(['marked_by_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'class_id', 'date', name='uq_attendance_date')
    )
    op.create_index(op.f('ix_attendance_date'), 'attendance', ['date'], unique=False)
    op.create_index(op.f('ix_attendance_student_id'), 'attendance', ['student_id'], unique=False)
    op.create_index(op.f('ix_attendance_class_id'), 'attendance', ['class_id'], unique=False)

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('school_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.String(36), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('old_values', sa.Text(), nullable=True),
        sa.Column('new_values', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_school_id'), 'audit_logs', ['school_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)


def downgrade() -> None:
    """Downgrade from revision 001: drop all tables."""
    op.drop_table('audit_logs')
    op.drop_table('attendance')
    op.drop_table('classes')
    op.drop_table('students')
    op.drop_table('users')
    op.drop_table('schools')
