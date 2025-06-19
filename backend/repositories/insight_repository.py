import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from datetime import datetime

from database import ClinicalInsight as DBClinicalInsight
from models.clinical_insight import ClinicalInsightCreate, ClinicalInsight # Pydantic models

class InsightRepository:
    """
    Repository class for ClinicalInsight data operations.
    Handles interaction with the database for ClinicalInsight entities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_insight(self, insight_data: ClinicalInsightCreate) -> DBClinicalInsight:
        """Creates a new clinical insight in the database."""
        insight_id = str(uuid.uuid4())
        new_insight = DBClinicalInsight(
            id=insight_id,
            user_id=insight_data.user_id,
            source_type=insight_data.source_type,
            source_id=insight_data.source_id,
            insight_text=insight_data.insight_text,
            severity=insight_data.severity,
            recommendations=insight_data.recommendations,
            created_at=datetime.utcnow()
        )
        self.db.add(new_insight)
        await self.db.commit()
        await self.db.refresh(new_insight)
        return new_insight

    async def get_insight_by_id(self, insight_id: str) -> Optional[DBClinicalInsight]:
        """Fetches a clinical insight by its ID."""
        stmt = select(DBClinicalInsight).where(DBClinicalInsight.id == insight_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_insights_by_user(self, user_id: str) -> List[DBClinicalInsight]:
        """Fetches all clinical insights for a specific user."""
        stmt = select(DBClinicalInsight).where(DBClinicalInsight.user_id == user_id).order_by(DBClinicalInsight.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_insight(self, insight_id: str, updates: dict) -> Optional[DBClinicalInsight]:
        """Updates an existing clinical insight."""
        stmt = update(DBClinicalInsight).where(DBClinicalInsight.id == insight_id).values(**updates).returning(DBClinicalInsight)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete_insight(self, insight_id: str) -> bool:
        """Deletes a clinical insight by its ID."""
        stmt = delete(DBClinicalInsight).where(DBClinicalInsight.id == insight_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0