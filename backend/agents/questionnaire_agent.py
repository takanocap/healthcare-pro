import asyncio
import json
from datetime import datetime
from google.cloud import pubsub_v1
from google.cloud import bigquery
from repositories.questionnaire_repository import QuestionnaireRepository
from repositories.insight_repository import InsightRepository
from services.insight_service import InsightService
from core.pubsub_client import PubSubClient
from core.websocket_manager import websocket_manager
from config import settings
from database import AsyncSessionLocal, create_db_and_tables # Import for DB session within agent
from models.questionnaire import Answer, QuestionnaireSession # Pydantic models for parsing
from models.clinical_insight import ClinicalInsightCreate # Pydantic insight model for creation


# --- Initialization for the agent ---
pubsub_client = PubSubClient()
bigquery_client = bigquery.Client(project=settings.GCP_PROJECT_ID)

async def get_insight_service_for_agent():
    """Helper to get InsightService with a new DB session for the agent."""
    async for db_session in AsyncSessionLocal():
        insight_repo = InsightRepository(db_session)
        yield InsightService(insight_repo, pubsub_client)

async def get_questionnaire_repo_for_agent():
    """Helper to get QuestionnaireRepository with a new DB session for the agent."""
    async for db_session in AsyncSessionLocal():
        yield QuestionnaireRepository(db_session)

# --- BigQuery Logging Function ---
async def log_questionnaire_activity_to_bigquery(user_id: str, session_id: str, activity_type: str, details: str):
    """Logs questionnaire activity to BigQuery."""
    table_id = f"{settings.GCP_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.{settings.BIGQUERY_TABLE_USER_ACTIVITY}"
    rows_to_insert = [{
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "activity_type": activity_type,
        "details": details
    }]
    try:
        errors = bigquery_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"BigQuery insert errors: {errors}")
        else:
            print(f"Logged questionnaire activity '{activity_type}' for user {user_id}, session {session_id} to BigQuery.")
    except Exception as e:
        print(f"Failed to log questionnaire activity to BigQuery: {e}")

# --- Pub/Sub Message Callback ---
async def process_new_answer(message: pubsub_v1.types.ReceivedMessage):
    """
    Callback function to process new answers from Pub/Sub.
    This simulates the Questionnaire Agent's logic.
    """
    print(f"Questionnaire Agent: Received answer: {message.data.decode('utf-8')}")
    try:
        message.ack()

        answer_data_raw = message.data.decode('utf-8')
        answer_dict = json.loads(answer_data_raw)
        parsed_answer = Answer(**answer_dict)

        session_id = parsed_answer.session_id
        question_id = parsed_answer.question_id
        answer_text = parsed_answer.answer_text

        # 1. Log answer submission to BigQuery
        async for q_repo in get_questionnaire_repo_for_agent():
            session = await q_repo.get_session_by_id(session_id)
            if session:
                user_id = session.user_id
                await log_questionnaire_activity_to_bigquery(
                    user_id,
                    session_id,
                    "answer_submitted",
                    f"Question ID: {question_id}, Answer: {answer_text}"
                )

                # Check if session is complete (this is a simplified check for demo)
                # In a real app, you'd fetch the questionnaire definition and compare
                # the number of submitted answers against the total questions.
                # For this example, let's assume a session is "complete" after X answers or explicitly marked.
                # Here, we'll just process answers. The frontend or another trigger would mark completion.

                # If the session is indeed completed (e.g., from an external trigger or determined here)
                # and you want to generate an insight from the whole session:
                # For demo, let's assume after *any* answer, we check if the session is done and generate insight if so.
                # REAL WORLD: This part would be more robust.

                # Simulate a simple check for completion or a trigger to analyze the whole session
                all_answers_for_session = await q_repo.get_answers_by_session(session_id)
                if len(all_answers_for_session) >= 3: # Arbitrary number for demo
                    print(f"Questionnaire Agent: Session {session_id} appears to be near completion or ready for analysis.")
                    full_session_data = {
                        "user_id": user_id,
                        "session_id": session_id,
                        "answers": [{"question_id": a.question_id, "answer_text": a.answer_text} for a in all_answers_for_session]
                    }
                    session_summary_text = f"User {user_id} completed a questionnaire session {session_id} with answers: {json.dumps(full_session_data['answers'])}"

                    async for insight_service in get_insight_service_for_agent():
                        insight_text_from_ai = await insight_service.generate_insight_with_ai(
                            user_id,
                            session_summary_text,
                            "questionnaire_summary",
                            session_id
                        )

                        insight_create_data = ClinicalInsightCreate(
                            user_id=user_id,
                            source_type="questionnaire_summary",
                            source_id=session_id,
                            insight_text=insight_text_from_ai,
                            severity="high" if "concern" in insight_text_from_ai.lower() else "low", # Simple AI output check
                            recommendations="Consider follow-up questions or intervention based on questionnaire responses."
                        )
                        new_insight = await insight_service.create_clinical_insight(insight_create_data)

                        if new_insight:
                            print(f"Questionnaire Agent: Generated and stored new insight for user {user_id} from session {session_id}: {new_insight.id}")
                            await websocket_manager.send_to_user(
                                user_id,
                                "new_clinical_insight",
                                {"insight": new_insight.model_dump()}
                            )
                        else:
                            print(f"Questionnaire Agent: Failed to create clinical insight from session.")
            else:
                print(f"Questionnaire Agent: Session {session_id} not found for answer.")

    except json.JSONDecodeError as e:
        print(f"Questionnaire Agent: Error decoding JSON: {e} - Message data: {message.data.decode('utf-8')}")
        message.nack()
    except Exception as e:
        print(f"Questionnaire Agent: An error occurred while processing answer: {e}")
        message.nack()

async def main_questionnaire_agent():
    """Main function to run the Questionnaire Agent."""
    print("Starting Questionnaire Agent...")
    await create_db_and_tables()

    subscription_path_new_answer = pubsub_client.subscriber.subscription_path(
        project=settings.GCP_PROJECT_ID,
        subscription="new-answer-subscription-questionnaire-agent" # This subscription needs to exist
    )

    streaming_pull_future = pubsub_client.subscribe(subscription_path_new_answer, process_new_answer)

    try:
        await streaming_pull_future.result()
    except asyncio.CancelledError:
        print("Questionnaire Agent: Streaming pull cancelled.")
    except Exception as e:
        print(f"Questionnaire Agent: Streaming pull encountered an exception: {e}")
    finally:
        streaming_pull_future.cancel()
        await streaming_pull_future
        pubsub_client.close()
        print("Questionnaire Agent stopped.")

if __name__ == "__main__":
    # To run this agent standalone for testing:
    # python -m agents.questionnaire_agent
    asyncio.run(main_questionnaire_agent())
