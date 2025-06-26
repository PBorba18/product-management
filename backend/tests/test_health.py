import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    return app

def test_health_endpoint(client):
    response = client.get('/api/health/')
    assert response.status_code == 200
    data = response.get_json()
    assert data.get('status') == 'healthy'

