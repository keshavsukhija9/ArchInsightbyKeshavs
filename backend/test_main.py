"""
Simple test to verify the main application works
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to ArchInsight API"
    assert "version" in data


def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data


def test_api_router_included():
    """Test that API routes are included"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
