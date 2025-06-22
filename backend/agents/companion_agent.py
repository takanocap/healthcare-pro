import asyncio
import json
from google.cloud import pubsub_v1
from google.cloud import bigquery
from sqlalchemy.ext.asyncio import AsyncSession # For potentially writing to DB (e.g., insights)
from repositories.insight_repository import InsightRepository
from services.insight_service import InsightService
from core.pubsub_client import PubSubClient
from core.websocket_manager import websocket_manager
from config import settings
from database import AsyncSessionLocal, create_db_and_tables # Import for DB session within agent
from models.message import Message # Pydantic message model for parsing
from models.clinical_insight import ClinicalInsightCreate # Pydantic insight model for creation


# --- Initialization for the agent ---
# These should be initialized once when the agent starts
pubsub_client = PubSubClient()
bigquery_client = bigquery.Client(project=settings.GCP_PROJECT_ID)

# For database interaction (e.g., creating insights)
async def get_insight_service_for_agent():
    """Helper to get InsightService with a new DB session for the agent."""
    async for db_session in AsyncSessionLocal():
        insight_repo = InsightRepository(db_session)
        yield InsightService(insight_repo, pubsub_client)

# --- BigQuery Logging Function ---
async def log_user_activity_to_bigquery(user_id: str, activity_type: str, details: str):
    """Logs user activity (e.g., messages) to BigQuery."""
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
            print(f"Logged user activity '{activity_type}' for {user_id} to BigQuery.")
    except Exception as e:
        print(f"Failed to log to BigQuery: {e}")

# --- Pub/Sub Message Callback ---
async def process_new_message(message: pubsub_v1.types.ReceivedMessage):
    """
    Callback function to process new messages from Pub/Sub.
    This simulates the Companion Agent's logic.
    """
    print(f"Companion Agent: Received message: {message.data.decode('utf-8')}")
    try:
        # Acknowledge the message immediately to prevent reprocessing
        message.ack()

        # Parse the message data
        message_data_raw = message.data.decode('utf-8')
        message_dict = json.loads(message_data_raw)
        parsed_message = Message(**message_dict)

        user_id = parsed_message.sender_id
        message_content = parsed_message.content

        # 1. Log activity to BigQuery
        await log_user_activity_to_bigquery(
            user_id,
            "new_chat_message",
            f"Message ID: {parsed_message.id}, Content: {message_content}"
        )

        # 2. Simulate AI analysis and generate insight (using InsightService)
        # We're manually getting the service here as agents run independently
        # In a more complex setup, you might have a dedicated DI for agents
        async for insight_service in get_insight_service_for_agent():
            insight_text_from_ai = await insight_service.generate_insight_with_ai(
                user_id,
                message_content,
                "message_analysis",
                parsed_message.id
            )

            # 3. Create the insight in the database (via InsightService)
            insight_create_data = ClinicalInsightCreate(
                user_id=user_id,
                source_type="message_analysis",
                source_id=parsed_message.id,
                insight_text=insight_text_from_ai,
                severity="medium", # Placeholder, AI would determine this
                recommendations="Observe user's emotional tone and frequency of communication."
            )
            new_insight = await insight_service.create_clinical_insight(insight_create_data)

            if new_insight:
                print(f"Companion Agent: Generated and stored new insight for user {user_id}: {new_insight.id}")
                # 4. Notify affected user via WebSocket
                await websocket_manager.send_to_user(
                    user_id,
                    "new_clinical_insight",
                    {"insight": new_insight.model_dump()}
                )
            else:
                print(f"Companion Agent: Failed to create clinical insight.")

        # Simulate a direct "companion" response if needed (optional)
        # If this agent also replies to users, it would publish a message to a 'companion_response' topic
        # and the frontend would consume that. For now, we only generate insights.

    except json.JSONDecodeError as e:
        print(f"Companion Agent: Error decoding JSON: {e} - Message data: {message.data.decode('utf-8')}")
        message.nack() # Negative acknowledge if message is malformed
    except Exception as e:
        print(f"Companion Agent: An error occurred while processing message: {e}")
        # Depending on error type, might nack or just log and ack
        message.nack() # If a transient error, nack to retry later

async def main_companion_agent():
    """Main function to run the Companion Agent."""
    print("Starting Companion Agent...")
    await create_db_and_tables() # Ensure tables exist for insight storage

    subscription_path_new_message = pubsub_client.subscriber.subscription_path(
        project=settings.GCP_PROJECT_ID,
        subscription="new-message-subscription-companion-agent" # This subscription needs to exist
    )

    # Start listening for messages. This call is blocking until the future is cancelled.
    streaming_pull_future = pubsub_client.subscribe(subscription_path_new_message, process_new_message)

    try:
        # Keep the agent running indefinitely
        await streaming_pull_future.result()
    except asyncio.CancelledError:
        print("Companion Agent: Streaming pull cancelled.")
    except Exception as e:
        print(f"Companion Agent: Streaming pull encountered an exception: {e}")
    finally:
        streaming_pull_future.cancel()
        await streaming_pull_future # Await the cancellation
        pubsub_client.close()
        print("Companion Agent stopped.")

if __name__ == "__main__":
    # To run this agent standalone for testing:
    # python -m agents.companion_agent
    asyncio.run(main_companion_agent())