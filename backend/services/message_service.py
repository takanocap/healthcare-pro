from typing import Optional, List
from repositories.message_repository import MessageRepository
from models.message import MessageCreate, Message # Pydantic models
from core.pubsub_client import PubSubClient # Import Pub/Sub client
from config import settings

class MessageService:
    """
    Service layer for Message-related business logic.
    Handles message creation, retrieval, and publishing to Pub/Sub.
    """
    def __init__(self, message_repo: MessageRepository, pubsub_client: PubSubClient):
        self.message_repo = message_repo
        self.pubsub_client = pubsub_client

    async def create_and_publish_message(self, message_data: MessageCreate) -> Optional[Message]:
        """
        Creates a message in the database and publishes it to Pub/Sub.
        """
        db_message = await self.message_repo.create_message(message_data)
        if db_message:
            # Convert SQLAlchemy model to Pydantic model for consistent Pub/Sub data
            message_pydantic = Message.model_validate(db_message)
            message_json = message_pydantic.model_dump_json()

            # Publish the message to Pub/Sub
            topic_path = self.pubsub_client.publisher.topic_path(
                project=settings.GCP_PROJECT_ID,
                topic=settings.PUBSUB_TOPIC_NEW_MESSAGE
            )
            future = self.pubsub_client.publish(topic_path, message_json.encode("utf-8"))
            
            try:
                # Google Pub/Sub futures are not awaitable; use result() instead
                message_id_in_pubsub = future.result()
                print(f"Published message {db_message.id} to Pub/Sub: {message_id_in_pubsub}")
            except Exception as e:
                print(f"Failed to publish message {db_message.id} to Pub/Sub: {e}")
                # Consider logging or rollback if publish is critical
            return None # Or raise an exception
        return None

    async def get_user_messages(self, user_id: str) -> List[Message]:
        """Retrieves all messages for a given user."""
        db_messages = await self.message_repo.get_messages_for_user(user_id)
        return [Message.model_validate(msg) for msg in db_messages]

    async def get_message_conversation(self, user1_id: str, user2_id: str) -> List[Message]:
        """Retrieves messages forming a conversation between two users."""
        db_messages = await self.message_repo.get_conversation(user1_id, user2_id)
        return [Message.model_validate(msg) for msg in db_messages]

    async def mark_message_as_read(self, message_id: str) -> Optional[Message]:
        """Marks a message as read."""
        db_message = await self.message_repo.mark_message_as_read(message_id)
        if db_message:
            return Message.model_validate(db_message)
        return None