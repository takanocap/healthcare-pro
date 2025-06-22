from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Pydantic models for questionnaire data

class Question(BaseModel):
    """Pydantic model for a single question within a questionnaire."""
    question_id: str
    question_text: str
    question_type: str # e.g., "text", "multiple_choice", "single_choice"
    options: Optional[List[str]] = None # For multiple/single choice questions

class QuestionnaireBase(BaseModel):
    """Base Pydantic model for Questionnaire data."""
    title: str = Field(min_length=3)
    description: Optional[str] = None
    questions: List[Question] # List of Question Pydantic models

class QuestionnaireCreate(QuestionnaireBase):
    """Pydantic model for creating a new Questionnaire."""
    pass

class Questionnaire(QuestionnaireBase):
    """Pydantic model for Questionnaire data retrieved from the database."""
    id: str
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
        json_dumps_extra = {"indent": 2} # For better JSON output of questions

class AnswerCreate(BaseModel):
    """Pydantic model for creating a new Answer."""
    session_id: str
    question_id: str
    answer_text: str

class Answer(AnswerCreate):
    """Pydantic model for Answer data retrieved from the database."""
    id: str
    timestamp: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True

class QuestionnaireSessionBase(BaseModel):
    """Base Pydantic model for QuestionnaireSession data."""
    user_id: str
    questionnaire_id: str

class QuestionnaireSessionCreate(QuestionnaireSessionBase):
    """Pydantic model for creating a new Questionnaire Session."""
    pass

class QuestionnaireSession(QuestionnaireSessionBase):
    """Pydantic model for Questionnaire Session data retrieved from the database."""
    id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str # e.g., "started", "completed", "aborted"

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True