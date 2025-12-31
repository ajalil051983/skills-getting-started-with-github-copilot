from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_adds_participant():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure email not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert res.json()["message"] == f"Signed up {email} for {activity}"

    # Verify GET /activities shows the new participant
    res2 = client.get("/activities")
    assert res2.status_code == 200
    data = res2.json()
    assert email in data[activity]["participants"]

    # Cleanup
    client.delete(f"/activities/{activity}/participants", params={"email": email})


def test_cannot_signup_twice():
    activity = "Chess Club"
    email = "duplicate@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200

    # Second signup should fail
    res2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res2.status_code == 400
    assert "already" in res2.json()["detail"].lower()

    # Cleanup
    client.delete(f"/activities/{activity}/participants", params={"email": email})
