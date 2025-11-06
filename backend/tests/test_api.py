from __future__ import annotations

from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app import auth, database, main
from backend.app.database import Base


def setup_test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    database.SessionLocal = TestingSessionLocal
    auth.SessionLocal = TestingSessionLocal
    return engine


def auth_header(client: TestClient, email: str, password: str) -> Dict[str, str]:
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_full_user_journey(tmp_path):
    engine = setup_test_db()
    client = TestClient(main.app)

    register_payload = {
        "email": "alice@example.com",
        "full_name": "Alice Zhang",
        "password": "StrongPass123",
        "target_exam": "CET-4",
    }
    response = client.post("/auth/register", json=register_payload)
    assert response.status_code == 201, response.text
    user_data = response.json()
    assert user_data["email"] == register_payload["email"]

    headers = auth_header(client, register_payload["email"], register_payload["password"])

    exam_payload = {"name": "Mock Exam", "description": "Practice exam"}
    response = client.post("/exams", json=exam_payload, headers=headers)
    assert response.status_code == 201, response.text
    exam_id = response.json()["id"]

    course_payload = {
        "exam_id": exam_id,
        "title": "Listening Skills",
        "level": "beginner",
        "description": "Improve listening",
    }
    response = client.post("/courses", json=course_payload, headers=headers)
    assert response.status_code == 201, response.text
    course_id = response.json()["id"]

    lesson_payload = {
        "course_id": course_id,
        "title": "Lesson 1",
        "content": "Introduction to listening",
        "duration_minutes": 30,
    }
    response = client.post("/lessons", json=lesson_payload, headers=headers)
    assert response.status_code == 201, response.text
    lesson_id = response.json()["id"]

    study_plan_payload = {
        "name": "CET-4 Sprint",
        "goal": "Finish in two weeks",
        "lesson_ids": [lesson_id],
    }
    response = client.post("/study-plans", json=study_plan_payload, headers=headers)
    assert response.status_code == 201, response.text
    plan_id = response.json()["id"]
    assert response.json()["lessons"][0]["id"] == lesson_id

    update_payload = {"name": "Updated Sprint", "lesson_ids": [lesson_id]}
    response = client.patch(f"/study-plans/{plan_id}", json=update_payload, headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Updated Sprint"

    summary_response = client.get("/dashboard/summary", headers=headers)
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["total_courses"] == 1
    assert summary["total_lessons"] == 1
    assert summary["total_study_plans"] == 1
    assert len(summary["upcoming_lessons"]) == 1

    seed_response = client.post("/seed/basic", headers=headers)
    assert seed_response.status_code == 201
    payload = seed_response.json()
    assert payload["status"] == "seeded"
    assert payload["demo_user"] in {"created", "existing"}

    seed_response_again = client.post("/seed/basic", headers=headers)
    assert seed_response_again.status_code == 201
    payload_again = seed_response_again.json()
    assert payload_again["status"] == "already_seeded"
    assert payload_again["demo_user"] in {"created", "existing"}

    engine.dispose()
