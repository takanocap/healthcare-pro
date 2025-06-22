import os
from pydantic_settings import BaseSettings


from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """
    Settings class to load environment variables for the application.
    Uses pydantic_settings for type checking and validation.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/healthcare_pro")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "hacker2025-team-152-dev")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")

    # Pub/Sub Topics
    PUBSUB_TOPIC_NEW_MESSAGE: str = os.getenv("PUBSUB_TOPIC_NEW_MESSAGE", "new_message_topic")
    PUBSUB_TOPIC_NEW_ANSWER: str = os.getenv("PUBSUB_TOPIC_NEW_ANSWER", "new_answer_topic")
    PUBSUB_TOPIC_CLINICAL_INSIGHT: str = os.getenv("PUBSUB_TOPIC_CLINICAL_INSIGHT", "clinical_insight_topic")

    # BigQuery Dataset and Tables
    BIGQUERY_DATASET_ID: str = os.getenv("BIGQUERY_DATASET_ID", "my_health_data")
    BIGQUERY_TABLE_USER_ACTIVITY: str = os.getenv("BIGQUERY_TABLE_USER_ACTIVITY", "user_activity_logs")
    BIGQUERY_TABLE_AGENT_INSIGHTS: str = os.getenv("BIGQUERY_TABLE_AGENT_INSIGHTS", "agent_insights")

    class Config:
        """
        Pydantic settings configuration.
        """
        case_sensitive = True # Environment variable names are case-sensitive

settings = Settings()