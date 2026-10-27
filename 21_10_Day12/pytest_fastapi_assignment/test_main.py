from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test GET /tasks
def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test GET /tasks/1
def test_get_task_by_id():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


# Test GET invalid task
def test_get_invalid_task():
    response = client.get("/tasks/999")

    assert response.status_code == 404


# Test POST /tasks
def test_create_task():
    new_task = {
        "id": 4,
        "title": "Check server logs",
        "status": "Pending"
    }

    response = client.post("/tasks", json=new_task)

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["title"] == "Check server logs"


# Test invalid POST data
def test_create_task_invalid():
    invalid_task = {
        "id": 5,
        "title": "Missing Status"
    }

    response = client.post("/tasks", json=invalid_task)

    assert response.status_code == 422


# Test PUT /tasks/2
def test_update_task():
    updated_task = {
        "id": 2,
        "title": "Review invoice",
        "status": "Completed"
    }

    response = client.put("/tasks/2", json=updated_task)

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


# Test DELETE /tasks/3
def test_delete_task():
    response = client.delete("/tasks/3")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


# Verify task 3 deleted
def test_deleted_task_not_found():
    response = client.get("/tasks/3")

    assert response.status_code == 404