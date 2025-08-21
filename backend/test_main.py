"""
Simple test to verify the main application works
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, base_url="http://test")


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "ArchInsight" in response.text


def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_router_included():
    """Test that the API router is included"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
