import json
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.insight_repository import InsightRepository
from models.clinical_insight import ClinicalInsightCreate, ClinicalInsight # Pydantic models
from core.pubsub_client import PubSubClient
from config import settings

# This import is for simulating Vertex AI calls.
# In a real scenario, you'd configure and use the AIPlatform client.
from google.cloud import aiplatform

class InsightService:
    """
    Service layer for Clinical Insight business logic.
    Handles creation, retrieval of insights, and interaction with AI for generation.
    """
    def __init__(self, insight_repo: InsightRepository, pubsub_client: PubSubClient):
        self.insight_repo = insight_repo
        self.pubsub_client = pubsub_client
        # Initialize Vertex AI client (or mock for simulation)
        # For actual usage, ensure gcloud is authenticated and project/region are set.
        # self.ai_client = aiplatform.gapic.PredictionServiceClient(
        #     client_options={"api_endpoint": f"{settings.GCP_REGION}-aiplatform.googleapis.com"}
        # )
        # self.model_path = self.ai_client.endpoint_path(
        #     project=settings.GCP_PROJECT_ID,
        #     location=settings.GCP_REGION,
        #     endpoint="your-llm-endpoint-id" # Replace with your deployed LLM endpoint ID
        # )

    async def generate_insight_with_ai(self, user_id: str, text_data: str, source_type: str, source_id: Optional[str] = None) -> str:
        """
        Simulates generating a clinical insight using an AI model (e.g., Vertex AI LLM).
        In a real scenario, this would call Vertex AI.
        """
        print(f"Simulating AI insight generation for user {user_id} based on '{source_type}' data...")
        prompt = f"Analyze the following patient data and provide a concise clinical insight and potential recommendations:\n\n{text_data}\n\nInsight:"

        # --- SIMULATED AI RESPONSE ---
        # Replace this with actual Vertex AI API call in production
        try:
            # Example for Vertex AI Text Generation (requires a deployed model)
            # from google.cloud.aiplatform.schema.predict.params import Content
            # response = self.ai_client.predict(
            #     endpoint=self.model_path,
            #     instances=[Content(text_content=prompt).to_dict()],
            #     parameters={"temperature": 0.2, "maxOutputTokens": 256}
            # )
            # generated_text = response.predictions[0]["content"]

            # For now, just a mock response
            generated_text = f"Simulated AI insight: Based on the {source_type} data, it appears there might be a minor concern regarding X. Further monitoring recommended. Recommendations: Encourage Y, advise Z."
            print(f"Simulated AI generated insight: {generated_text[:100]}...")
            return generated_text
        except Exception as e:
            print(f"Error calling Vertex AI (or simulation): {e}")
            return "AI insight generation failed due to an error."
        # --- END SIMULATED AI RESPONSE ---

    async def create_clinical_insight(self, insight_data: ClinicalInsightCreate) -> Optional[ClinicalInsight]:
        """
        Creates a new clinical insight in the database and publishes it to Pub/Sub.
        """
        db_insight = await self.insight_repo.create_insight(insight_data)
        if db_insight:
            insight_pydantic = ClinicalInsight.model_validate(db_insight)
            insight_json = insight_pydantic.model_dump_json()

            topic_path = self.pubsub_client.publisher.topic_path(
                project=settings.GCP_PROJECT_ID,
                topic=settings.PUBSUB_TOPIC_CLINICAL_INSIGHT
            )
            future = self.pubsub_client.publish(topic_path, insight_json.encode("utf-8"))
            try:
                await future
                print(f"Published insight {db_insight.id} to Pub/Sub.")
            except Exception as e:
                print(f"Failed to publish insight {db_insight.id} to Pub/Sub: {e}")
                return None

            return ClinicalInsight.model_validate(db_insight)
        return None

    async def get_user_insights(self, user_id: str) -> List[ClinicalInsight]:
        """Retrieves all clinical insights for a given user."""
        db_insights = await self.insight_repo.get_insights_by_user(user_id)
        return [ClinicalInsight.model_validate(insight) for insight in db_insights]

    async def get_insight(self, insight_id: str) -> Optional[ClinicalInsight]:
        """Retrieves a single clinical insight by ID."""
        db_insight = await self.insight_repo.get_insight_by_id(insight_id)
        if db_insight:
            return ClinicalInsight.model_validate(db_insight)
        return None