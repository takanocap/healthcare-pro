from google.cloud import pubsub_v1
import asyncio
from typing import Callable, Awaitable
from concurrent.futures import Future

class PubSubClient:
    """
    A wrapper class for Google Cloud Pub/Sub Publisher and Subscriber clients.
    """
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        print("PubSubClient initialized.")

    def publish(self, topic_path: str, data: bytes, **attrs) -> Future:
        """
        Publishes a message to the specified Pub/Sub topic.
        Args:
            topic_path (str): The full Pub/Sub topic path (e.g., projects/PROJECT_ID/topics/TOPIC_ID).
            data (bytes): The message payload.
            **attrs: Additional attributes for the message.
        Returns:
            concurrent.futures.Future: A future object representing the publish operation.
        """
        future = self.publisher.publish(topic_path, data, **attrs)
        return future

    def subscribe(self, subscription_path: str, callback: Callable[[pubsub_v1.types.ReceivedMessage], Awaitable[None]]):
        """
        Subscribes to a Pub/Sub subscription and starts an asynchronous message pull.
        Args:
            subscription_path (str): The full Pub/Sub subscription path.
            callback (Callable): An asynchronous callback function to process received messages.
                                  It should accept a pubsub_v1.types.ReceivedMessage object.
        """
        # The 'flow_control' parameter controls how many messages are pulled concurrently.
        # It's important for managing resource usage and preventing starvation.
        # max_messages: The maximum number of messages that the consumer can have outstanding.
        # max_bytes: The maximum number of bytes that the consumer can have outstanding.
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback,
            flow_control=pubsub_v1.types.FlowControl(max_messages=10)
        )
        print(f"Listening for messages on {subscription_path}...")

        # Return the future so the caller can manage its lifecycle (e.g., await it to keep listening)
        return streaming_pull_future

    def close(self):
        """Closes the Pub/Sub clients."""
        print("Closing PubSubClient.")
        self.publisher.api.transport.close()
        self.subscriber.api.transport.close()

# Instantiate the PubSubClient globally or as a dependency
pubsub_client = PubSubClient()
