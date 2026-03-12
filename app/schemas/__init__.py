"""
Pydantic request/response schemas.

Used for request validation and response documentation.
Separated by entity type.
"""

from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr


# ============ Base Schemas ============
class BaseResponse(BaseModel):
    """Base response model with common fields."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ School Schemas ============
class SchoolCreate(BaseModel):
    """Create school request."""

    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    timezone: str = "UTC"


class SchoolResponse(BaseResponse):
    """School response."""

    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    timezone: str


# ============ User Schemas ============
class UserCreate(BaseModel):
    """Create user request."""

    email: EmailStr
    password: str
    full_name: str
    role: str  # admin, teacher, parent, student
    school_id: str


class UserResponse(BaseResponse):
    """User response (no password)."""

    email: str
    full_name: str
    role: str
    school_id: str
    is_active: bool
    last_login: Optional[datetime] = None


class UserLogin(BaseModel):
    """Login request."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Update user request."""

    full_name: Optional[str] = None
    is_active: Optional[bool] = None


# ============ Student Schemas ============
class StudentCreate(BaseModel):
    """Create student request."""

    school_id: str
    student_id: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentResponse(BaseResponse):
    """Student response."""

    school_id: str
    student_id: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    enrollment_date: Optional[date] = None
    is_active: bool


class StudentUpdate(BaseModel):
    """Update student request."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    is_active: Optional[bool] = None


# ============ Class Schemas ============
class ClassCreate(BaseModel):
    """Create class request."""

    school_id: str
    name: str
    code: str
    teacher_id: str
    grade_level: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None


class ClassResponse(BaseResponse):
    """Class response."""

    school_id: str
    name: str
    code: str
    teacher_id: str
    grade_level: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None
    is_active: bool


class ClassUpdate(BaseModel):
    """Update class request."""

    name: Optional[str] = None
    code: Optional[str] = None
    teacher_id: Optional[str] = None
    grade_level: Optional[str] = None
    room_number: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


# ============ Attendance Schemas ============
class AttendanceCreate(BaseModel):
    """Create attendance record request."""

    student_id: str
    class_id: str
    date: date
    status: str  # present, absent, excused, late
    notes: Optional[str] = None


class AttendanceResponse(BaseResponse):
    """Attendance response."""

    student_id: str
    class_id: str
    date: date
    status: str
    marked_by_user_id: str
    notes: Optional[str] = None


class AttendanceUpdate(BaseModel):
    """Update attendance record request."""

    status: Optional[str] = None
    notes: Optional[str] = None


# ============ Audit Log Schemas ============
class AuditLogResponse(BaseResponse):
    """Audit log response."""

    school_id: str
    user_id: str
    entity_type: str
    entity_id: str
    action: str
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
