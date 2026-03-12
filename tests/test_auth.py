"""
Authentication endpoint tests.

Tests for login, refresh token, and logout stubs.
Will be expanded when auth implementation is complete.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestAuth:
    """Authentication endpoint tests (stubs)."""

    def test_login_not_implemented(self, client):
        """Test that /auth/login returns 501 Not Implemented (stub)."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 501
        data = response.json()
        assert "detail" in data

    def test_refresh_token_not_implemented(self, client):
        """Test that /auth/refresh returns 501 Not Implemented (stub)."""
        response = client.post(
            "/api/v1/auth/refresh",
            params={"refresh_token": "dummy_token"},
        )
        assert response.status_code == 501

    def test_logout_not_implemented(self, client):
        """Test that /auth/logout returns 501 Not Implemented (stub)."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 501

    def test_get_current_user_not_implemented(self, client):
        """Test that /users/me returns 501 Not Implemented (stub)."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 501


class TestStudentRoutes:
    """Student endpoint tests (stubs)."""

    def test_list_students_not_implemented(self, client):
        """Test that GET /students returns 501 Not Implemented (stub)."""
        response = client.get("/api/v1/students")
        assert response.status_code == 501

    def test_create_student_not_implemented(self, client):
        """Test that POST /students returns 501 Not Implemented (stub)."""
        response = client.post(
            "/api/v1/students",
            json={
                "school_id": "school-1",
                "student_id": "S001",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        assert response.status_code == 501


class TestAttendanceRoutes:
    """Attendance endpoint tests (stubs)."""

    def test_list_attendance_not_implemented(self, client):
        """Test that GET /attendance returns 501 Not Implemented (stub)."""
        response = client.get("/api/v1/attendance")
        assert response.status_code == 501

    def test_mark_attendance_not_implemented(self, client):
        """Test that POST /attendance returns 501 Not Implemented (stub)."""
        response = client.post(
            "/api/v1/attendance",
            json={
                "student_id": "student-1",
                "class_id": "class-1",
                "date": "2026-03-12",
                "status": "present",
            },
        )
        assert response.status_code == 501
