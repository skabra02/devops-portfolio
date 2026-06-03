import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- health endpoint ---

def test_health_returns_200(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_health_returns_ok_status(client):
    data = response = client.get('/health').get_json()
    assert data['status'] == 'ok'

# --- GET /tasks ---

def test_get_tasks_returns_200(client):
    response = client.get('/tasks')
    assert response.status_code == 200

def test_get_tasks_returns_list(client):
    data = client.get('/tasks').get_json()
    assert 'tasks' in data
    assert isinstance(data['tasks'], list)

# --- POST /tasks ---

def test_create_task_returns_201(client):
    response = client.post('/tasks',
        json={'title': 'Learn Docker'},
        content_type='application/json'
    )
    assert response.status_code == 201

def test_create_task_returns_task_object(client):
    response = client.post('/tasks',
        json={'title': 'Learn Kubernetes'},
        content_type='application/json'
    )
    data = response.get_json()
    assert 'task' in data
    assert data['task']['title'] == 'Learn Kubernetes'
    assert data['task']['done'] == False
    assert 'id' in data['task']

def test_create_task_missing_title_returns_400(client):
    response = client.post('/tasks',
        json={},
        content_type='application/json'
    )
    assert response.status_code == 400

def test_create_task_empty_body_returns_400(client):
    response = client.post('/tasks',
        data='not json',
        content_type='application/json'
    )
    assert response.status_code == 400
