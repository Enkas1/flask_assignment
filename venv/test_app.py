import pytest
import json
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_route_not_found(client):
    response = client.get("/routedoesntexist")
    assert response.status_code == 404
    assert b"Route not found. Check if you spelled it correctly" in response.data


def test_authentication(client):
    response = client.get("/tasks", headers={"Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="})
    assert response.status_code == 200   # dXNlcm5hbWU6cGFzc3dvcmQ= är "username:password" i Base64 encoding.


def test_get_tasks(client):
    response = client.get("/tasks")
    data = json.loads(response.data)
    assert isinstance(data, dict)


def test_post_invalid_tasks(client):
    data = {
        "description": "Test task",
        "category": "Test category",
        "invalid_key": "Invalid data"
    }
    response = client.post("/tasks", json=data)
    assert response.status_code == 400
    assert b"Invalid key" in response.data


def test_get_nonexistent_task_id(client):
    response = client.get("/tasks/100")
    assert response.status_code == 404
    assert b"Found no task with id" in response.data


def test_delete_task(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 401
    assert b"Unauthorized" in response.data


def test_put_task(client):
    data = {
        "description": "Updated task description",
        "category": "Updated category",
        "invalid_key": "Invalid data"
    }
    response = client.put("/tasks/100", json=data)
    assert response.status_code == 404
    assert b"Found no task with id" in response.data


def test_task_complete_nonexistent_task(client):
    response = client.put("/tasks/100/complete")
    assert response.status_code == 404
    assert b"Found no task with id" in response.data


def test_categories_key(client):
    response = client.get("/tasks/categories")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "categories" in data  #Kollar om categories key finns i data.
    assert isinstance(data["categories"], list)


def test_get_tasks_by_nonexistent_category(client):
    response = client.get("/tasks/categories/TestCategory")
    assert response.status_code == 404
    assert b"Found no category with the name" in response.data


def test_completed_or_not(client):
    response = client.get("/tasks/completedornot")
    assert response.status_code == 200

    data = response.get_json()
    assert "completed tasks" in data
    assert "Unfinished tasks" in data
