import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_load_data(client):
    response = client.get("/load_data")
    assert response.status_code == 200
    assert response.json() == {"message": "Data loaded successfully"}
