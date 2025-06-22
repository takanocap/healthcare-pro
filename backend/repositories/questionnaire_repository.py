import uuid
import json
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from datetime import datetime

from database import Questionnaire as DBQuestionnaire
from database import QuestionnaireSession as DBQuestionnaireSession
from database import Answer as DBAnswer
from models.questionnaire import (
    QuestionnaireCreate, Questionnaire,
    QuestionnaireSessionCreate, QuestionnaireSession,
    AnswerCreate, Answer
)

class QuestionnaireRepository:
    """
    Repository class for Questionnaire, Session, and Answer data operations.
    Handles interaction with the database for these entities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- Questionnaire CRUD ---
    async def create_questionnaire(self, questionnaire_data: QuestionnaireCreate) -> DBQuestionnaire:
        """Creates a new questionnaire."""
        q_id = str(uuid.uuid4())
        new_q = DBQuestionnaire(
            id=q_id,
            title=questionnaire_data.title,
            description=questionnaire_data.description,
            questions_json=json.dumps([q.model_dump() for q in questionnaire_data.questions])
        )
        self.db.add(new_q)
        await self.db.commit()
        await self.db.refresh(new_q)
        return new_q

    async def get_questionnaire_by_id(self, q_id: str) -> Optional[DBQuestionnaire]:
        """Fetches a questionnaire by its ID."""
        stmt = select(DBQuestionnaire).where(DBQuestionnaire.id == q_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all_questionnaires(self) -> List[DBQuestionnaire]:
        """Fetches all questionnaires."""
        stmt = select(DBQuestionnaire)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_questionnaire(self, q_id: str, updates: dict) -> Optional[DBQuestionnaire]:
        """Updates an existing questionnaire."""
        if "questions" in updates:
            updates["questions_json"] = json.dumps([q.model_dump() for q in updates["questions"]])
            del updates["questions"] # Remove Pydantic object before passing to SQLAlchemy
        stmt = update(DBQuestionnaire).where(DBQuestionnaire.id == q_id).values(**updates).returning(DBQuestionnaire)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete_questionnaire(self, q_id: str) -> bool:
        """Deletes a questionnaire by its ID."""
        stmt = delete(DBQuestionnaire).where(DBQuestionnaire.id == q_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    # --- Questionnaire Session CRUD ---
    async def create_session(self, session_data: QuestionnaireSessionCreate) -> DBQuestionnaireSession:
        """Creates a new questionnaire session."""
        session_id = str(uuid.uuid4())
        new_session = DBQuestionnaireSession(
            id=session_id,
            user_id=session_data.user_id,
            questionnaire_id=session_data.questionnaire_id,
            started_at=datetime.utcnow(),
            status="started"
        )
        self.db.add(new_session)
        await self.db.commit()
        await self.db.refresh(new_session)
        return new_session

    async def get_session_by_id(self, session_id: str) -> Optional[DBQuestionnaireSession]:
        """Fetches a questionnaire session by its ID."""
        stmt = select(DBQuestionnaireSession).where(DBQuestionnaireSession.id == session_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_sessions_by_user(self, user_id: str) -> List[DBQuestionnaireSession]:
        """Fetches all sessions for a specific user."""
        stmt = select(DBQuestionnaireSession).where(DBQuestionnaireSession.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_session(self, session_id: str, updates: dict) -> Optional[DBQuestionnaireSession]:
        """Updates an existing questionnaire session."""
        stmt = update(DBQuestionnaireSession).where(DBQuestionnaireSession.id == session_id).values(**updates).returning(DBQuestionnaireSession)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    # --- Answer CRUD ---
    async def create_answer(self, answer_data: AnswerCreate) -> DBAnswer:
        """Creates a new answer for a questionnaire session."""
        answer_id = str(uuid.uuid4())
        new_answer = DBAnswer(
            id=answer_id,
            session_id=answer_data.session_id,
            question_id=answer_data.question_id,
            answer_text=answer_data.answer_text,
            timestamp=datetime.utcnow()
        )
        self.db.add(new_answer)
        await self.db.commit()
        await self.db.refresh(new_answer)
        return new_answer

    async def get_answers_by_session(self, session_id: str) -> List[DBAnswer]:
        """Fetches all answers for a specific questionnaire session."""
        stmt = select(DBAnswer).where(DBAnswer.session_id == session_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()