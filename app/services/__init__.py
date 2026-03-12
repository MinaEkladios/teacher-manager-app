"""
Business logic and service layer.

Services handle CRUD operations and business rules:
- UserService: User management, password hashing, role validation
- StudentService: Student profiles, enrollment
- ClassService: Class management, enrollment
- AttendanceService: Attendance marking, reports
- AuditService: Audit logging with compliance tracking

Stubs for full implementation in Phase 2C+.
"""

from typing import Optional
from abc import ABC, abstractmethod


class BaseService(ABC):
    """Abstract base for all services."""

    @abstractmethod
    async def create(self, obj_in):
        """Create entity."""
        pass

    @abstractmethod
    async def read(self, id: str):
        """Read entity by ID."""
        pass

    @abstractmethod
    async def update(self, id: str, obj_in):
        """Update entity."""
        pass

    @abstractmethod
    async def delete(self, id: str):
        """Delete entity."""
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100):
        """List entities with pagination."""
        pass


class UserService(BaseService):
    """User management service."""

    async def create(self, obj_in):
        """Create user (stub).
        
        Implementation in Phase 2C+:
        - Hash password
        - Validate role
        - Create audit log
        """
        raise NotImplementedError()

    async def read(self, id: str):
        """Read user by ID (stub)."""
        raise NotImplementedError()

    async def update(self, id: str, obj_in):
        """Update user (stub)."""
        raise NotImplementedError()

    async def delete(self, id: str):
        """Delete user (stub)."""
        raise NotImplementedError()

    async def list(self, skip: int = 0, limit: int = 100):
        """List users (stub)."""
        raise NotImplementedError()

    async def authenticate(self, email: str, password: str):
        """Authenticate user by email/password (stub).
        
        Implementation:
        - Look up user by email
        - Verify password hash
        - Update last_login
        - Return user
        """
        raise NotImplementedError()


class StudentService(BaseService):
    """Student profile management service."""

    async def create(self, obj_in):
        """Create student (stub).
        
        Implementation:
        - Generate unique student ID if needed
        - Validate school exists
        - Create audit log
        """
        raise NotImplementedError()

    async def read(self, id: str):
        """Read student by ID (stub)."""
        raise NotImplementedError()

    async def update(self, id: str, obj_in):
        """Update student (stub)."""
        raise NotImplementedError()

    async def delete(self, id: str):
        """Delete student (stub)."""
        raise NotImplementedError()

    async def list(self, skip: int = 0, limit: int = 100, school_id: Optional[str] = None):
        """List students by school (stub)."""
        raise NotImplementedError()

    async def bulk_import(self, file_path: str, school_id: str):
        """Bulk import students from CSV (stub).
        
        Implementation:
        - Parse CSV
        - Validate rows
        - Create students
        - Return report
        """
        raise NotImplementedError()


class ClassService(BaseService):
    """Class / course management service."""

    async def create(self, obj_in):
        """Create class (stub)."""
        raise NotImplementedError()

    async def read(self, id: str):
        """Read class by ID (stub)."""
        raise NotImplementedError()

    async def update(self, id: str, obj_in):
        """Update class (stub)."""
        raise NotImplementedError()

    async def delete(self, id: str):
        """Delete class (stub)."""
        raise NotImplementedError()

    async def list(self, skip: int = 0, limit: int = 100, school_id: Optional[str] = None):
        """List classes by school (stub)."""
        raise NotImplementedError()

    async def add_student(self, class_id: str, student_id: str):
        """Enroll student in class (stub).
        
        Implementation:
        - Create ClassEnrollment row
        - Validate capacity
        """
        raise NotImplementedError()


class AttendanceService(BaseService):
    """Attendance marking and reporting service."""

    async def create(self, obj_in):
        """Mark attendance (stub).
        
        Implementation:
        - Validate student, class, date
        - Check for duplicates
        - Create audit log
        """
        raise NotImplementedError()

    async def read(self, id: str):
        """Read attendance record (stub)."""
        raise NotImplementedError()

    async def update(self, id: str, obj_in):
        """Update attendance record (stub)."""
        raise NotImplementedError()

    async def delete(self, id: str):
        """Delete attendance record (stub)."""
        raise NotImplementedError()

    async def list(self, skip: int = 0, limit: int = 100, class_id: Optional[str] = None):
        """List attendance by class (stub)."""
        raise NotImplementedError()

    async def get_attendance_report(self, class_id: str, month: Optional[str] = None):
        """Generate attendance report (stub).
        
        Implementation:
        - Aggregate attendance by student
        - Calculate percentages
        - Flag absences
        - Return PDF-ready data
        """
        raise NotImplementedError()

    async def trigger_absence_alert(self, student_id: str):
        """Trigger alert for excessive absences (stub).
        
        Implementation:
        - Check absence count
        - Send email/SMS to parent/teacher
        - Log notification
        """
        raise NotImplementedError()


class AuditService(BaseService):
    """Audit logging service for compliance."""

    async def create(self, obj_in):
        """Create audit log entry (stub)."""
        raise NotImplementedError()

    async def read(self, id: str):
        """Read audit log (stub)."""
        raise NotImplementedError()

    async def update(self, id: str, obj_in):
        """Update not supported for audit logs."""
        raise NotImplementedError("Audit logs are immutable")

    async def delete(self, id: str):
        """Delete not supported for audit logs."""
        raise NotImplementedError("Audit logs are immutable")

    async def list(self, skip: int = 0, limit: int = 100, school_id: Optional[str] = None):
        """List audit logs (stub)."""
        raise NotImplementedError()

    async def log_action(self, school_id: str, user_id: str, entity_type: str, 
                         entity_id: str, action: str, old_values: Optional[str] = None,
                         new_values: Optional[str] = None, ip_address: Optional[str] = None):
        """Log audit event (stub).
        
        Implementation:
        - Create AuditLog row
        - Serialize old/new values to JSON
        - Index by timestamp
        """
        raise NotImplementedError()
