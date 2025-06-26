# agents/companion_agent.py
import os
from typing import Optional
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()
model_name = os.getenv("MODEL")


class CompanionAgent:
    """Agent that initiates the check-in process"""
    def __init__(self):
        # Define agent
        self.agent = Agent(
            name="HealthcareCompanion",
            model=model_name,
            instruction="""
            You are a compassionate healthcare companion agent specialized in
            patient-reported outcomes (PROs) for chronic care patients.
            Your role:
            - Initiate friendly, conversational check-ins
            - Adapt your tone based on patient's emotional state
            - Support multilingual communication
            - Ensure privacy and build trust
            - Collect initial assessment data

            Always be empathetic, respectful, and encourage honest communication.
            """
        )
        # Setup in-memory session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="healthcare_companion",
            session_service=self.session_service
        )

    async def initiate_checkin(self, patient_data: dict, message: Optional[str]) -> dict:
        """Initiate conversational check-in with patient"""
        user_id = patient_data.get('id', 'user_123')
        session = await self.session_service.create_session(
            user_id=user_id,
            app_name="healthcare_companion"
        )

        # User message as content
        user_message = types.Content(
            role='user',
            parts=[types.Part(text=message or "Hi")]
        )

        # Run the agent with the input
        events = self.runner.run(
            user_id=user_id,
            session_id=session.id,
            new_message=user_message
        )

        # Extract the final LLM response
        final_response = next(
            (e.content.parts[0].text for e in events if e.is_final_response())
        )

        return {
            "message": final_response,
            "next_action": "adaptive_questionnaire",
            "patient_id": patient_data.get('id')
        }
