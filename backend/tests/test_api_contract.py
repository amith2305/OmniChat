from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reset_history_accepts_json_body_session_id():
    session_id = "contract-session"
    response = client.post("/api/history/reset", json={"session_id": session_id})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["session_id"] == session_id
    assert payload["reset"] is True
