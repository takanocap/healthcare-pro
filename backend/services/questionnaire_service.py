import json
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.questionnaire_repository import QuestionnaireRepository
from models.questionnaire import (
    QuestionnaireCreate, Questionnaire,
    QuestionnaireSessionCreate, QuestionnaireSession,
    AnswerCreate, Answer
)
from core.pubsub_client import PubSubClient
from config import settings

class QuestionnaireService:
    """
    Service layer for Questionnaire-related business logic.
    Handles questionnaire creation, session management, answer submission,
    and publishing events to Pub/Sub.
    """
    def __init__(self, q_repo: QuestionnaireRepository, pubsub_client: PubSubClient):
        self.q_repo = q_repo
        self.pubsub_client = pubsub_client

    async def create_questionnaire(self, questionnaire_data: QuestionnaireCreate) -> Optional[Questionnaire]:
        """Creates a new questionnaire."""
        db_q = await self.q_repo.create_questionnaire(questionnaire_data)
        if db_q:
            return Questionnaire.model_validate(db_q)
        return None

    async def get_questionnaire(self, q_id: str) -> Optional[Questionnaire]:
        """Retrieves a questionnaire by ID."""
        db_q = await self.q_repo.get_questionnaire_by_id(q_id)
        if db_q:
            # Deserialize questions_json back to list of Question Pydantic models
            q_dict = db_q.__dict__
            q_dict["questions"] = json.loads(q_dict["questions_json"])
            del q_dict["questions_json"]
            return Questionnaire.model_validate(q_dict)
        return None

    async def get_all_questionnaires(self) -> List[Questionnaire]:
        """Retrieves all questionnaires."""
        db_qs = await self.q_repo.get_all_questionnaires()
        result_list = []
        for db_q in db_qs:
            q_dict = db_q.__dict__.copy()
            q_dict["questions"] = json.loads(q_dict["questions_json"])
            del q_dict["questions_json"]
            result_list.append(Questionnaire.model_validate(q_dict))
        return result_list

    async def start_questionnaire_session(self, session_data: QuestionnaireSessionCreate) -> Optional[QuestionnaireSession]:
        """Starts a new questionnaire session for a user."""
        db_session = await self.q_repo.create_session(session_data)
        if db_session:
            return QuestionnaireSession.model_validate(db_session)
        return None

    async def submit_answer(self, answer_data: AnswerCreate) -> Optional[Answer]:
        """
        Submits an answer to a questionnaire session and publishes it to Pub/Sub.
        """
        db_answer = await self.q_repo.create_answer(answer_data)
        if db_answer:
            # Check if this answer completes the session (optional, requires logic to compare against questionnaire questions)
            # For simplicity, we just publish the answer. A separate agent will process completed sessions.

            answer_pydantic = Answer.model_validate(db_answer)
            answer_json = answer_pydantic.model_dump_json()

            topic_path = self.pubsub_client.publisher.topic_path(
                project=settings.GCP_PROJECT_ID,
                topic=settings.PUBSUB_TOPIC_NEW_ANSWER
            )
            future = self.pubsub_client.publish(topic_path, answer_json.encode("utf-8"))
            try:
                await future
                print(f"Published answer {db_answer.id} to Pub/Sub.")
            except Exception as e:
                print(f"Failed to publish answer {db_answer.id} to Pub/Sub: {e}")
                return None

            return Answer.model_validate(db_answer)
        return None

    async def complete_session(self, session_id: str) -> Optional[QuestionnaireSession]:
        """Marks a questionnaire session as completed."""
        updates = {"completed_at": datetime.utcnow(), "status": "completed"}
        db_session = await self.q_repo.update_session(session_id, updates)
        if db_session:
            return QuestionnaireSession.model_validate(db_session)
        return None

    async def get_session_answers(self, session_id: str) -> List[Answer]:
        """Retrieves all answers for a given session."""
        db_answers = await self.q_repo.get_answers_by_session(session_id)
        return [Answer.model_validate(ans) for ans in db_answers]

    async def get_user_sessions(self, user_id: str) -> List[QuestionnaireSession]:
        """Retrieves all questionnaire sessions for a user."""
        db_sessions = await self.q_repo.get_sessions_by_user(user_id)
        return [QuestionnaireSession.model_validate(sess) for sess in db_sessions]
