"""
SQLAlchemy ORM Models.

Core data models:
- School: Multi-school support
- User: Admin, teacher, parent, student
- Student: Student profiles
- Class: Classes / groups
- Attendance: Attendance records
- AuditLog: Audit trail for compliance
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Integer, Enum, Text, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class School(Base):
    """School/organization entity."""

    __tablename__ = "schools"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<School id={self.id} name={self.name}>"


class User(Base):
    """User entity (admin, teacher, parent, student)."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", "school_id", name="uq_user_email_school"),)

    id = Column(String(36), primary_key=True)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, index=True)  # admin, teacher, parent, student
    is_active = Column(Boolean, default=True, index=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"


class Student(Base):
    """Student entity."""

    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("student_id", "school_id", name="uq_student_id_school"),)

    id = Column(String(36), primary_key=True)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    student_id = Column(String(50), nullable=False)  # School student ID / enrollment number
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date)
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    parent_email = Column(String(255))
    parent_phone = Column(String(20))
    enrollment_date = Column(Date)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Student id={self.id} name={self.first_name} {self.last_name}>"


class Class(Base):
    """Class / course entity."""

    __tablename__ = "classes"

    id = Column(String(36), primary_key=True)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, index=True)
    teacher_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    grade_level = Column(String(50))
    room_number = Column(String(50))
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Class id={self.id} name={self.name}>"


class Attendance(Base):
    """Attendance record."""

    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("student_id", "class_id", "date", name="uq_attendance_date"),)

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False, index=True)
    class_id = Column(String(36), ForeignKey("classes.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(50), nullable=False)  # present, absent, excused, late
    marked_by_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Attendance student={self.student_id} date={self.date} status={self.status}>"


class AuditLog(Base):
    """Audit log for compliance and tracking."""

    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    entity_type = Column(String(50), nullable=False)  # User, Student, Attendance, etc.
    entity_id = Column(String(36), nullable=False)
    action = Column(String(50), nullable=False)  # create, update, delete
    old_values = Column(Text)  # JSON string of previous values
    new_values = Column(Text)  # JSON string of new values
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<AuditLog user={self.user_id} action={self.action} entity={self.entity_type}>"
