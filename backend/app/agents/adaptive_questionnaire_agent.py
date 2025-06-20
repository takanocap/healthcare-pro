# agents/adaptive_questionnaire_agent.py
import os
from typing import List, Optional
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()
model_name = os.getenv("MODEL")


class AdaptiveQuestionnaireAgent:
    """Starts a questionnaire for the patient based on the trigger."""
    def __init__(self):
        self.agent = Agent(
            name="AdaptiveQuestionnaire",
            model=model_name,
            instruction="""
            You are an adaptive questionnaire agent that personalizes PRO surveys
            based on patient responses and comprehension signals.

            Capabilities:
            - Adjust question complexity based on patient understanding
            - Modify tone and approach based on emotional cues
            - Support accessibility requirements
            - Ensure clinical relevance while maintaining engagement
            - Adapt delivery mode (text, simplified language, etc.)
            """
        )
        # Setup session, in-memory session service and runner
        self.session = None
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="healthcare_companion",
            session_service=self.session_service
        )

    async def generate_adaptive_questions(self, patient_context: dict,
                                          message: Optional[str]) -> dict:
        """Generate personalized questions based on patient context"""
        user_id = patient_context.get('id', 'user_123')
        if not self.session:
            session = await self.session_service.create_session(
                user_id=user_id,
                app_name="healthcare_companion"
            )
            self.session = session

        # User message as content
        user_message = types.Content(
            role='user',
            parts=[types.Part(text=message or "Hi")]
        )

        # Run the agent with the input
        events = self.runner.run(
            user_id=user_id,
            session_id=self.session.id,
            new_message=user_message
        )

        # Extract the final LLM response
        final_response = next(
            (e.content.parts[0].text for e in events if e.is_final_response())
        )

        return {
            "message": final_response,
            "next_action": "trend_monitoring",
            "patient_id": patient_context.get('id')
        }
