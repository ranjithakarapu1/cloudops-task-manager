import os
os.environ["DATABASE_URL"] = "sqlite:///./test_tasks.db"
os.environ["UPLOAD_DIR"] = "./test_uploads"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_list_task():
    response = client.post("/tasks", json={"title": "Learn ALB", "description": "Test health checks"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    assert client.get(f"/tasks/{task_id}").status_code == 200
