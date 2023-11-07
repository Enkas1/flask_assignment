import pytest
import json
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_tasks(client):
    response = client.get('/tasks')
    data = json.loads(response.data)
    assert isinstance(data, dict)


def test_post_tasks(client):
    data = {
        "description": "Test task",
        "category": "Test category"
    }
    response = client.post('/tasks', json=data)
    assert response.status_code == 200


def test_get_task_id(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200


def test_delete_task(client):
    response = client.delete('/tasks/1')
    assert response.status_code == 200



def test_put_task(client):
    data = {
        "description": "Updated task description",
        "category": "Updated category"
    }
    response = client.put('/tasks/1', json=data)
    assert response.status_code == 200


def test_task_complete(client):
    response = client.put('/tasks/1/complete')
    assert response.status_code == 200


def test_categories(client):
    response = client.get('/tasks/categories')
    assert response.status_code == 200

    data = json.loads(response.data)  #Kollar om categories key finns i data.
    assert "categories" in data
    assert isinstance(data["categories"], list)


def test_get_tasks_by_category(client):
    response = client.get('/tasks/categories/TestCategory')
    assert response.status_code == 200



def test_completed_or_not(client):
    response = client.get('/tasks/completedornot')
    assert response.status_code == 200

    data = response.get_json()
    assert "completed tasks" in data
    assert "Unfinished tasks" in data
