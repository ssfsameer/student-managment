from fastapi.testclient import TestClient

from app.main import app, students


client = TestClient(app)


def setup_function():
    students.clear()


def test_get_students_empty():
    response = client.get("/students")

    assert response.status_code == 200
    assert response.json() == []


def test_create_student_success():
    student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.75
    }

    response = client.post("/students", json=student)

    assert response.status_code == 201
    assert response.json() == student


def test_get_student_success():
    student = {
        "id": 1,
        "name": "Karim Hasan",
        "department": "EEE",
        "semester": 4,
        "cgpa": 3.50
    }

    client.post("/students", json=student)

    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json() == student


def test_update_student_success():
    student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.50
    }

    client.post("/students", json=student)

    updated_student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.80
    }

    response = client.put("/students/1", json=updated_student)

    assert response.status_code == 200
    assert response.json() == updated_student


def test_delete_student_success():
    student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.75
    }

    client.post("/students", json=student)

    response = client.delete("/students/1")

    assert response.status_code == 200
    assert response.json() == student

    get_response = client.get("/students/1")

    assert get_response.status_code == 404


def test_get_nonexistent_student():
    response = client.get("/students/999")

    assert response.status_code == 404


def test_create_duplicate_student_id():
    student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.75
    }

    client.post("/students", json=student)

    response = client.post("/students", json=student)

    assert response.status_code == 400


def test_update_nonexistent_student():
    student = {
        "id": 999,
        "name": "Unknown Student",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.50
    }

    response = client.put("/students/999", json=student)

    assert response.status_code == 404


def test_delete_nonexistent_student():
    response = client.delete("/students/999")

    assert response.status_code == 404


def test_update_student_with_different_id():
    student = {
        "id": 1,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 5,
        "cgpa": 3.75
    }

    client.post("/students", json=student)

    updated_student = {
        "id": 2,
        "name": "Rahim Ahmed",
        "department": "CSE",
        "semester": 6,
        "cgpa": 3.90
    }

    response = client.put("/students/1", json=updated_student)

    assert response.status_code == 400