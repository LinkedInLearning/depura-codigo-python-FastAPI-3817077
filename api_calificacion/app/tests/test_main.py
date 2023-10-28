from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": "Restaurant Review API", "version": "1.0.0"}
