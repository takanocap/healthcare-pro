
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.agents.orchestrator import HealthcarePROOrchestrator

@pytest.fixture
def orchestrator():
    with patch("app.agents.orchestrator.CompanionAgent") as MockCompanion, \
         patch("app.agents.orchestrator.AdaptiveQuestionnaireAgent") as MockQuestionnaire, \
         patch("app.agents.orchestrator.LlmAgent"):
        mock_companion = MockCompanion.return_value
        mock_questionnaire = MockQuestionnaire.return_value
        orchestrator = HealthcarePROOrchestrator()
        orchestrator.companion = mock_companion
        orchestrator.questionnaire = mock_questionnaire
        return orchestrator

@pytest.mark.asyncio
async def test_handle_patient_interaction_checkin(orchestrator):
    orchestrator.companion.initiate_checkin = AsyncMock(return_value={"result": "checkin"})
    result = await orchestrator.handle_patient_interaction(
        {"id": "123"}, "checkin", "hello"
    )
    orchestrator.companion.initiate_checkin.assert_awaited_once_with({"id": "123"}, "hello")
    assert result == {"result": "checkin"}

@pytest.mark.asyncio
async def test_handle_patient_interaction_questionnaire(orchestrator):
    orchestrator.questionnaire.generate_adaptive_questions = AsyncMock(return_value={"result": "questionnaire"})
    result = await orchestrator.handle_patient_interaction(
        {"id": "123"}, "questionnaire", "start"
    )
    orchestrator.questionnaire.generate_adaptive_questions.assert_awaited_once_with({"id": "123"}, "start")
    assert result == {"result": "questionnaire"}

@pytest.mark.asyncio
async def test_handle_patient_interaction_trend_analysis(orchestrator):
    orchestrator._get_historical_data = AsyncMock(return_value=[{"data": 1}])
    orchestrator.trend_monitor = MagicMock()
    orchestrator.trend_monitor.analyze_trends = AsyncMock(return_value={"result": "trend"})
    patient_data = {"id": "123"}
    result = await orchestrator.handle_patient_interaction(
        patient_data, "trend_analysis", None
    )
    orchestrator._get_historical_data.assert_awaited_once_with("123")
    orchestrator.trend_monitor.analyze_trends.assert_awaited_once_with("123", [{"data": 1}])
    assert result == {"result": "trend"}

@pytest.mark.asyncio
async def test_handle_patient_interaction_default(orchestrator):
    orchestrator.companion.initiate_checkin = AsyncMock(return_value={"result": "default"})
    result = await orchestrator.handle_patient_interaction(
        {"id": "123"}, "unknown_type", "msg"
    )
    orchestrator.companion.initiate_checkin.assert_awaited_once_with({"id": "123"}, "msg")
    assert result == {"result": "default"}

@pytest.mark.asyncio
async def test_get_patient_responses_not_implemented(orchestrator):
    with pytest.raises(NotImplementedError):
        await orchestrator._get_patient_responses("123")

@pytest.mark.asyncio
async def test_get_historical_data_not_implemented(orchestrator):
    with pytest.raises(NotImplementedError):
        await orchestrator._get_historical_data("123")