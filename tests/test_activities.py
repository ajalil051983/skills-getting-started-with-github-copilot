from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_structure():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Ensure a known activity exists
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_unregister_removes_participant():
    activity = "Programming Class"
    email = "removeme@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Add participant
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200

    # Verify participant present
    res2 = client.get("/activities")
    data = res2.json()
    assert email in data[activity]["participants"]

    # Unregister
    r2 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r2.status_code == 200

    # Verify removed
    res3 = client.get("/activities")
    data3 = res3.json()
    assert email not in data3[activity]["participants"]


def test_unregister_nonexistent_email_returns_400():
    activity = "Gym Class"
    email = "nobody@example.com"

    # Ensure email not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 400
    assert "not signed up" in r.json()["detail"].lower()


def test_signup_nonexistent_activity_returns_404():
    res = client.post(f"/activities/NoSuchActivity/signup", params={"email": "x@y.com"})
    assert res.status_code == 404


def test_unregister_nonexistent_activity_returns_404():
    res = client.delete(f"/activities/NoSuchActivity/participants", params={"email": "x@y.com"})
    assert res.status_code == 404
