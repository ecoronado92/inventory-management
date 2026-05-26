"""
Tests for tasks API endpoints.
"""
import pytest


class TestTasksEndpoints:
    """Test suite for task-related endpoints."""

    def test_get_all_tasks(self, client):
        """Test getting all tasks."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Verify structure of first task
        first_task = data[0]
        assert "id" in first_task
        assert "title" in first_task
        assert "priority" in first_task
        assert "dueDate" in first_task
        assert "status" in first_task

    def test_task_field_types_and_values(self, client):
        """Test that task fields have proper types and constrained values."""
        response = client.get("/api/tasks")
        data = response.json()

        valid_priorities = ["high", "medium", "low"]
        valid_statuses = ["pending", "completed"]

        for task in data:
            assert isinstance(task["id"], int)
            assert isinstance(task["title"], str)
            assert len(task["title"]) > 0
            assert task["priority"].lower() in valid_priorities
            assert task["status"].lower() in valid_statuses
            # Due date should be ISO format (YYYY-MM-DD)
            assert "2025-" in task["dueDate"]

    def test_create_task(self, client):
        """Test creating a new task."""
        new_task = {
            "title": "Test task from pytest",
            "priority": "high",
            "dueDate": "2025-11-01"
        }
        response = client.post("/api/tasks", json=new_task)
        assert response.status_code == 201

        created = response.json()
        assert created["title"] == new_task["title"]
        assert created["priority"] == new_task["priority"]
        assert created["dueDate"] == new_task["dueDate"]
        assert created["status"] == "pending"
        # Server-assigned ids start above 100 so they never collide with the
        # client-side mock user tasks (ids 1-4) managed locally by the frontend
        assert created["id"] > 100

        # Verify it appears in the task list
        list_response = client.get("/api/tasks")
        task_ids = [task["id"] for task in list_response.json()]
        assert created["id"] in task_ids

        # Clean up so other tests see the original dataset
        delete_response = client.delete(f"/api/tasks/{created['id']}")
        assert delete_response.status_code == 200

    def test_create_task_missing_fields(self, client):
        """Test that creating a task without required fields fails validation."""
        response = client.post("/api/tasks", json={"title": "Incomplete task"})
        assert response.status_code == 422

    def test_toggle_task(self, client):
        """Test toggling a task between pending and completed."""
        # Get an existing task
        tasks = client.get("/api/tasks").json()
        task = tasks[0]
        original_status = task["status"]
        toggled_status = "completed" if original_status == "pending" else "pending"

        # Toggle once
        response = client.patch(f"/api/tasks/{task['id']}")
        assert response.status_code == 200
        assert response.json()["status"] == toggled_status

        # Toggle back to restore original state
        response = client.patch(f"/api/tasks/{task['id']}")
        assert response.status_code == 200
        assert response.json()["status"] == original_status

    def test_toggle_nonexistent_task(self, client):
        """Test toggling a task that doesn't exist."""
        response = client.patch("/api/tasks/999999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_delete_task(self, client):
        """Test deleting a task."""
        # Create a task to delete so the seed data is untouched
        created = client.post("/api/tasks", json={
            "title": "Task to delete",
            "priority": "low",
            "dueDate": "2025-12-01"
        }).json()

        response = client.delete(f"/api/tasks/{created['id']}")
        assert response.status_code == 200

        # Verify it no longer appears in the task list
        task_ids = [task["id"] for task in client.get("/api/tasks").json()]
        assert created["id"] not in task_ids

        # Deleting again should return 404
        response = client.delete(f"/api/tasks/{created['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist."""
        response = client.delete("/api/tasks/999999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
