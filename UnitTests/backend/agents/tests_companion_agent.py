import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from backend.app.agents.companion_agent import CompanionAgent

@pytest.fixture
def mock_agent():
    with patch("backend.app.agents.companion_agent.Agent") as MockAgent:
        yield MockAgent

@pytest.fixture
def mock_runner():
    with patch("backend.app.agents.companion_agent.Runner") as MockRunner:
        yield MockRunner

@pytest.fixture
def mock_session_service():
    with patch("backend.app.agents.companion_agent.InMemorySessionService") as MockSessionService:
        yield MockSessionService

@pytest.fixture
def mock_types():
    with patch("backend.app.agents.companion_agent.types") as mock_types:
        yield mock_types

def test_companion_agent_init(mock_agent, mock_runner, mock_session_service):
    agent_instance = CompanionAgent()
    assert hasattr(agent_instance, "agent")
    assert hasattr(agent_instance, "session_service")
    assert hasattr(agent_instance, "runner")
    # Check correct types
    mock_agent.assert_called_once()
    mock_session_service.assert_called_once()
    mock_runner.assert_called_once()

@pytest.mark.asyncio
async def test_initiate_checkin_success(
    mock_agent, mock_runner, mock_session_service, mock_types
):
    # Arrange
    agent_instance = CompanionAgent()

    # Mock session_service.create_session
    mock_session = MagicMock()
    mock_session.id = "session_1"
    agent_instance.session_service.create_session = AsyncMock(return_value=mock_session)

    # Mock types.Content and types.Part
    mock_content = MagicMock()
    mock_part = MagicMock()
    mock_types.Content.return_value = mock_content
    mock_types.Part.return_value = mock_part

    # Mock runner.run to yield events
    mock_event_final = MagicMock()
    mock_event_final.is_final_response.return_value = True
    mock_event_final.content.parts = [MagicMock(text="Hello, patient!")]
    agent_instance.runner.run = MagicMock(return_value=[mock_event_final])

    patient_data = {"id": "patient_42"}
    message = "How are you?"

    # Act
    result = await agent_instance.initiate_checkin(patient_data, message)

    # Assert
    agent_instance.session_service.create_session.assert_awaited_once_with(
        user_id="patient_42", app_name="healthcare_companion"
    )
    mock_types.Content.assert_called_once()
    agent_instance.runner.run.assert_called_once()
    assert result == {
        "message": "Hello, patient!",
        "next_action": "adaptive_questionnaire",
        "patient_id": "patient_42"
    }

@pytest.mark.asyncio
async def test_initiate_checkin_default_message(
    mock_agent, mock_runner, mock_session_service, mock_types
):
    agent_instance = CompanionAgent()
    mock_session = MagicMock()
    mock_session.id = "session_2"
    agent_instance.session_service.create_session = AsyncMock(return_value=mock_session)
    mock_types.Content.return_value = MagicMock()
    mock_types.Part.return_value = MagicMock()
    mock_event_final = MagicMock()
    mock_event_final.is_final_response.return_value = True
    mock_event_final.content.parts = [MagicMock(text="Hi there!")]
    agent_instance.runner.run = MagicMock(return_value=[mock_event_final])

    patient_data = {}
    message = None

    result = await agent_instance.initiate_checkin(patient_data, message)
    assert result["message"] == "Hi there!"
    assert result["patient_id"] is None