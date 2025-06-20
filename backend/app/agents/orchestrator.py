# agents/orchestrator.py
import os
from typing import List, Optional
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from app.agents.companion_agent import CompanionAgent
from app.agents.adaptive_questionnaire_agent import AdaptiveQuestionnaireAgent


load_dotenv()
model_name = os.getenv("MODEL")


class HealthcarePROOrchestrator:
    """Root orchestrator agent handles delegation"""
    def __init__(self):
        self.companion = CompanionAgent()
        self.questionnaire = AdaptiveQuestionnaireAgent()

        # Create agent team for coordination.
        self.agent_team = LlmAgent(
            name="orchestrator",
            # model="gemini-1.5-flash",
            model=model_name,
            instruction="""
            You are the orchestrator for a healthcare system.
            - Delegate emotional support and general chat to 'companion'.
            - Delegate health questionnaires to 'questionnaire'.
            - Delegate trend analysis or monitoring to 'trend_monitor'.
            Choose the right agent based on the user input.
            """,
            sub_agents=[
                self.companion.agent,
                self.questionnaire.agent,
            ]
        )

    async def handle_patient_interaction(self, patient_data: dict,
                                         interaction_type: str, user_message: Optional[str]) -> dict:
        """Orchestrate multi-agent interaction based on type"""

        if interaction_type == "checkin":
            return await self.companion.initiate_checkin(patient_data, user_message)

        if interaction_type == "questionnaire":
            return await self.questionnaire.generate_adaptive_questions(
                patient_data, user_message
            )

        # Default to companion agent
        return await self.companion.initiate_checkin(patient_data, user_message)

    async def _get_patient_responses(self, patient_id: str) -> List[dict]:
        """Fetch patient's previous responses from database"""
        # Implementation depends on your SQLAlchemy models
        pass

    async def _get_historical_data(self, patient_id: str) -> List[dict]:
        """Fetch historical PRO data for trend analysis"""
        # Implementation depends on your SQLAlchemy models
        pass
