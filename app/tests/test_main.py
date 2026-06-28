from fastapi.testclient import TestClient
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "environment" in data
    assert data["status"] == "healthy"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_env():
    response = client.get("/env")
    assert response.status_code == 200
    data = response.json()
    assert "ENVIRONMENT" in data
    assert "DB_HOST" in data
