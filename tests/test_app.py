import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert f"Signed up {email}" in r.json()["message"]
    # Duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400
    # Unregister
    r3 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r3.status_code == 200
    assert f"Unregistered {email}" in r3.json()["message"]
    # Unregister again should fail
    r4 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r4.status_code == 404
