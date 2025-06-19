from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClinicalInsightBase(BaseModel):
    """Base Pydantic model for ClinicalInsight data."""
    user_id: str
    source_type: str = Field(description="e.g., 'message_analysis', 'questionnaire_summary'")
    source_id: Optional[str] = Field(None, description="ID of the message/session that triggered insight")
    insight_text: str = Field(min_length=1)
    severity: Optional[str] = Field(None, description="e.g., 'low', 'medium', 'high'")
    recommendations: Optional[str] = None

class ClinicalInsightCreate(ClinicalInsightBase):
    """Pydantic model for creating a new ClinicalInsight."""
    pass

class ClinicalInsight(ClinicalInsightBase):
    """Pydantic model for ClinicalInsight data retrieved from the database."""
    id: str
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True