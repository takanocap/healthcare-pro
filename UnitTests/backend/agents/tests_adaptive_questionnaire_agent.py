import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.app.agents.adaptive_questionnaire_agent import AdaptiveQuestionnaireAgent

@pytest.fixture
def agent():
    return AdaptiveQuestionnaireAgent()

@patch("backend.app.agents.adaptive_questionnaire_agent.Agent")
@patch("backend.app.agents.adaptive_questionnaire_agent.InMemorySessionService")
@patch("backend.app.agents.adaptive_questionnaire_agent.Runner")
def test_init_sets_up_agent_and_runner(mock_runner, mock_session_service, mock_agent):
    instance = AdaptiveQuestionnaireAgent()
    assert instance.agent == mock_agent.return_value
    assert instance.session_service == mock_session_service.return_value
    assert instance.runner == mock_runner.return_value
    assert instance.session is None

@pytest.mark.asyncio
@patch("backend.app.agents.adaptive_questionnaire_agent.types")
@patch("backend.app.agents.adaptive_questionnaire_agent.Runner")
@patch("backend.app.agents.adaptive_questionnaire_agent.InMemorySessionService")
async def test_generate_adaptive_questions_creates_session_and_returns_response(
    mock_session_service, mock_runner, mock_types
):
    # Arrange
    agent = AdaptiveQuestionnaireAgent()
    agent.session_service = mock_session_service.return_value
    agent.runner = mock_runner.return_value

    # Mock session creation
    mock_session = MagicMock()
    mock_session.id = "session_1"
    agent.session = None
    agent.session_service.create_session = AsyncMock(return_value=mock_session)

    # Mock user message
    mock_content = MagicMock()
    mock_types.Content.return_value = mock_content

    # Mock events
    mock_event = MagicMock()
    mock_event.is_final_response.return_value = True
    mock_event.content.parts = [MagicMock(text="Adaptive question")]
    agent.runner.run.return_value = [mock_event]

    patient_context = {"id": "patient_42"}
    message = "Hello"

    # Act
    result = await agent.generate_adaptive_questions(patient_context, message)

    # Assert
    agent.session_service.create_session.assert_awaited_once_with(
        user_id="patient_42", app_name="healthcare_companion"
    )
    agent.runner.run.assert_called_once()
    assert result == {
        "message": "Adaptive question",
        "next_action": "trend_monitoring",
        "patient_id": "patient_42"
    }

@pytest.mark.asyncio
@patch("backend.app.agents.adaptive_questionnaire_agent.types")
@patch("backend.app.agents.adaptive_questionnaire_agent.Runner")
@patch("backend.app.agents.adaptive_questionnaire_agent.InMemorySessionService")
async def test_generate_adaptive_questions_uses_existing_session(
    mock_session_service, mock_runner, mock_types
):
    agent = AdaptiveQuestionnaireAgent()
    agent.session_service = mock_session_service.return_value
    agent.runner = mock_runner.return_value

    # Pre-existing session
    mock_session = MagicMock()
    mock_session.id = "session_2"
    agent.session = mock_session

    # Mock user message
    mock_content = MagicMock()
    mock_types.Content.return_value = mock_content

    # Mock events
    mock_event = MagicMock()
    mock_event.is_final_response.return_value = True
    mock_event.content.parts = [MagicMock(text="Follow-up question")]
    agent.runner.run.return_value = [mock_event]

    patient_context = {"id": "patient_99"}
    message = None  # Should default to "Hi"

    result = await agent.generate_adaptive_questions(patient_context, message)

    agent.runner.run.assert_called_once()
    assert result["message"] == "Follow-up question"
    assert result["next_action"] == "trend_monitoring"
    assert result["patient_id"] == "patient_99"