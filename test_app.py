import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Event Scheduler API is running!" in response.data

def test_create_event(client):
    data = {
        "title": "Test Event",
        "description": "Pytest check",
        "start_time": "2025-07-01T10:00:00",
        "end_time": "2025-07-01T11:00:00"
    }
    response = client.post('/events', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    res_data = response.get_json()
    assert res_data['title'] == "Test Event"

def test_get_events(client):
    response = client.get('/events')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_search_events(client):
    response = client.get('/events/search?q=Test')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
