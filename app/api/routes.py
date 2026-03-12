"""
API route definitions.

Will be expanded to include:
- Authentication (login, refresh, logout)
- Attendance management
- Student profiles
- Classes & schedules
- Reports & analytics
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["api"])


# ============ Schema Stubs ============
class LoginRequest(BaseModel):
    """Login request schema."""

    email: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    id: str
    email: str
    full_name: str
    role: str  # admin, teacher, parent, student
    school_id: str


# ============ Auth Routes (Stubs) ============
@router.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
async def login(request: LoginRequest):
    """Login endpoint (stub).
    
    Full implementation in Phase 2B.2:
    - Verify email/password
    - Generate JWT + refresh token
    - Return tokens
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login endpoint not yet implemented",
    )


@router.post("/auth/refresh", response_model=TokenResponse, tags=["Auth"])
async def refresh_token(refresh_token: str):
    """Refresh access token (stub).
    
    Full implementation in Phase 2B.2:
    - Validate refresh token
    - Issue new access token
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh endpoint not yet implemented",
    )


@router.post("/auth/logout", tags=["Auth"])
async def logout():
    """Logout endpoint (stub).
    
    Full implementation:
    - Blacklist refresh token (optional)
    - Clear session
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Logout endpoint not yet implemented",
    )


# ============ User Routes (Stubs) ============
@router.get("/users/me", response_model=UserResponse, tags=["Users"])
async def get_current_user():
    """Get current user profile (stub).
    
    Requires valid access token (JWT auth middleware).
    Full implementation in Phase 2B.2.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get current user not yet implemented",
    )


# ============ Attendance Routes (Stubs) ============
@router.get("/attendance", tags=["Attendance"])
async def list_attendance():
    """List attendance records (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Attendance listing not yet implemented",
    )


@router.post("/attendance", tags=["Attendance"])
async def mark_attendance():
    """Mark attendance (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Attendance marking not yet implemented",
    )


# ============ Student Profiles (Stubs) ============
@router.get("/students", tags=["Students"])
async def list_students():
    """List students (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Student listing not yet implemented",
    )


@router.post("/students", tags=["Students"])
async def create_student():
    """Create student (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Student creation not yet implemented",
    )


# ============ Classes & Schedules (Stubs) ============
@router.get("/classes", tags=["Classes"])
async def list_classes():
    """List classes (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Class listing not yet implemented",
    )


@router.post("/classes", tags=["Classes"])
async def create_class():
    """Create class (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Class creation not yet implemented",
    )


# ============ Reports & Analytics (Stubs) ============
@router.get("/reports/attendance", tags=["Reports"])
async def get_attendance_report():
    """Get attendance report (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Attendance report not yet implemented",
    )


@router.get("/reports/analytics", tags=["Reports"])
async def get_analytics():
    """Get analytics dashboard data (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Analytics not yet implemented",
    )
