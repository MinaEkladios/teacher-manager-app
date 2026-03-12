"""
Health check endpoint tests.

Basic tests for the /health and / root endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealth:
    """Health check endpoint tests."""

    def test_health_check_returns_200(self, client):
        """Test that /health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, client):
        """Test that /health response has required fields."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "ok"
        assert "app" in data
        assert "environment" in data

    def test_health_check_app_name(self, client):
        """Test that /health returns correct app name."""
        response = client.get("/health")
        data = response.json()
        
        assert data["app"] == "TeacherManager"


class TestRoot:
    """Root endpoint tests."""

    def test_root_returns_200(self, client):
        """Test that / endpoint returns 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_response_structure(self, client):
        """Test that / response has required fields."""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "docs" in data
        assert "openapi" in data

    def test_root_docs_link(self, client):
        """Test that / response includes correct docs link."""
        response = client.get("/")
        data = response.json()
        
        assert data["docs"] == "/docs"
        assert data["openapi"] == "/openapi.json"
