import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock
from backend.app.main import app, get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import UserLogin

# Use TestClient for sync endpoints
client = TestClient(app)

# Mock database dependency
def override_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def user_login_data():
    return {
        "username": "testuser",
        "date_of_birth": "1990-01-01"
    }

def test_login_existing_user(user_login_data):
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = user_login_data["username"]
    mock_user.date_of_birth = user_login_data["date_of_birth"]

    db = MagicMock()
    db.query().filter_by().first.return_value = mock_user

    with patch("backend.app.main.get_db", return_value=iter([db])):
        response = client.post("/login", json=user_login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_login_data["username"]
        assert data["date_of_birth"] == user_login_data["date_of_birth"]
        assert data["condition"] == "Hypertension"
        assert data["language"] == "English"

def test_login_new_user(user_login_data):
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    # Simulate new user after refresh
    new_user = MagicMock(spec=User)
    new_user.id = 2
    new_user.username = user_login_data["username"]
    new_user.date_of_birth = user_login_data["date_of_birth"]
    db.refresh.side_effect = lambda user: setattr(user, "id", 2)

    with patch("backend.app.main.get_db", return_value=iter([db])):
        with patch("backend.app.main.User", return_value=new_user):
            response = client.post("/login", json=user_login_data)
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == user_login_data["username"]
            assert data["date_of_birth"] == user_login_data["date_of_birth"]
            assert data["condition"] == "Hypertension"
            assert data["language"] == "English"

@pytest.mark.asyncio
async def test_interact_with_agent_success():
    request_data = {
        "patient_id": "p1",
        "interaction_type": "checkin",
        "patient_data": {"bp": 120},
        "user_message": "How am I doing?"
    }
    mock_response = {
        "result": "ok",
        "next_action": "continue"
    }

    with patch("backend.app.main.orchestrator") as mock_orchestrator:
        mock_orchestrator.handle_patient_interaction = AsyncMock(return_value=mock_response)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/agent/interact", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert data["agent_response"] == mock_response
            assert data["next_action"] == "continue"
            assert "metadata" in data

@pytest.mark.asyncio
async def test_interact_with_agent_exception():
    request_data = {
        "patient_id": "p1",
        "interaction_type": "checkin",
        "patient_data": {"bp": 120},
        "user_message": "How am I doing?"
    }

    with patch("backend.app.main.orchestrator") as mock_orchestrator:
        mock_orchestrator.handle_patient_interaction = AsyncMock(side_effect=Exception("fail"))
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/agent/interact", json=request_data)
            assert response.status_code == 500
            assert response.json()["detail"] == "fail"

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/agent/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "agents": "ready"}