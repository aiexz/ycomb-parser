from fastapi.testclient import TestClient


def test_comments(app: "TestClient"):
    response = app.get("/comments")
    assert response.status_code == 200
    x = response.json()
    assert len(x) == 10


def test_comments_by_user(app: "TestClient"):
    response = app.get("/comments/user/a0")
    assert response.status_code == 200
    x = response.json()
    assert len(x) >= 1


# def test_health(app: "TestClient"):
#     response = app.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}
