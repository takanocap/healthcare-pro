import socketio
from typing import Dict, Any

# This creates an AsyncServer instance suitable for ASGI applications like FastAPI.
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# The ASGI application that the FastAPI app will mount.
socket_app = socketio.ASGIApp(sio, other_asgi_app=None)

class WebSocketManager:
    """
    Manages WebSocket connections and broadcasting messages using Socket.IO.
    """
    def __init__(self):
        print("WebSocketManager initialized.")

        @sio.event
        async def connect(sid, environ):
            """Handle new WebSocket connections."""
            user_id = environ.get('HTTP_X_USER_ID') # Get user ID from headers if passed
            print(f"Client connected: {sid} (User ID: {user_id})")
            if user_id:
                sio.enter_room(sid, user_id) # Join a room named after the user ID

        @sio.event
        async def disconnect(sid):
            """Handle WebSocket disconnections."""
            print(f"Client disconnected: {sid}")

        @sio.event
        async def chat_message(sid, data):
            """Handle incoming chat messages from clients."""
            # This is an example of an event received from a client.
            # In a real app, you might validate data and then broadcast.
            print(f"Received chat message from {sid}: {data}")
            # Example: Echo back to the sender
            # await sio.emit('response_message', {'status': 'received', 'message': data}, room=sid)

    async def broadcast_message(self, event: str, data: Dict[str, Any]):
        """
        Broadcasts a message to all connected clients.
        """
        print(f"Broadcasting event '{event}' with data: {data}")
        await sio.emit(event, data)

    async def send_to_user(self, user_id: str, event: str, data: Dict[str, Any]):
        """
        Sends a message to all connections associated with a specific user ID.
        Clients should join rooms based on their user ID upon connection.
        """
        print(f"Sending event '{event}' to user '{user_id}' with data: {data}")
        await sio.emit(event, data, room=user_id)

websocket_manager = WebSocketManager()
