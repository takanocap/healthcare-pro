from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db, create_db_and_tables
from repositories.user_repository import UserRepository
from repositories.message_repository import MessageRepository
from repositories.questionnaire_repository import QuestionnaireRepository
from repositories.insight_repository import InsightRepository
from services.user_service import UserService
from services.message_service import MessageService
from services.questionnaire_service import QuestionnaireService
from services.insight_service import InsightService
from models.user import UserCreate, User # For request/response models
from models.message import MessageCreate, Message
from models.questionnaire import QuestionnaireCreate, Questionnaire, QuestionnaireSessionCreate, QuestionnaireSession, AnswerCreate, Answer
from models.clinical_insight import ClinicalInsightCreate, ClinicalInsight

from core.websocket_manager import socket_app, websocket_manager
from core.pubsub_client import pubsub_client
from config import settings
from config import settings  # Ensure settings.DATABASE_URL uses asyncpg, e.g., "postgresql+asyncpg://user:pass@host/db"
# Initialize FastAPI app
app = FastAPI(
    title="My Health Backend API",
    description="API for managing user data, messages, questionnaires, and clinical insights.",
    version="1.0.0"
)

# --- CORS Middleware ---
# Allows requests from your frontend application. Adjust origins as needed.
origins = [
    "http://localhost",
    "http://localhost:3000", # Example for a React/Vue frontend
    "http://localhost:8080", # Example for another local dev server
    # Add your deployed frontend URL here, e.g., "https://your-frontend.appspot.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the Socket.IO ASGI app onto the FastAPI app
# Mount the Socket.IO ASGI app onto the FastAPI app
app.mount("/ws", socket_app)  # All Socket.IO traffic will go through /ws
# --- Dependency Injection Functions ---

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Dependency that provides a UserRepository instance."""
    return UserRepository(db)

async def get_message_repository(db: AsyncSession = Depends(get_db)) -> MessageRepository:
    """Dependency that provides a MessageRepository instance."""
    return MessageRepository(db)

async def get_questionnaire_repository(db: AsyncSession = Depends(get_db)) -> QuestionnaireRepository:
    """Dependency that provides a QuestionnaireRepository instance."""
    return QuestionnaireRepository(db)

async def get_insight_repository(db: AsyncSession = Depends(get_db)) -> InsightRepository:
    """Dependency that provides an InsightRepository instance."""
    return InsightRepository(db)

async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """Dependency that provides a UserService instance."""
    return UserService(user_repo)

async def get_message_service(
    message_repo: MessageRepository = Depends(get_message_repository),
    pubsub: pubsub_client = Depends(lambda: pubsub_client) # Use the global instance
) -> MessageService:
    """Dependency that provides a MessageService instance."""
    return MessageService(message_repo, pubsub)

async def get_questionnaire_service(
    q_repo: QuestionnaireRepository = Depends(get_questionnaire_repository),
    pubsub: pubsub_client = Depends(lambda: pubsub_client)
) -> QuestionnaireService:
    """Dependency that provides a QuestionnaireService instance."""
    return QuestionnaireService(q_repo, pubsub)

async def get_insight_service(
    insight_repo: InsightRepository = Depends(get_insight_repository),
    pubsub: pubsub_client = Depends(lambda: pubsub_client)
) -> InsightService:
    """Dependency that provides an InsightService instance."""
    return InsightService(insight_repo, pubsub)

# --- Application Lifecycle Events ---

@app.on_event("startup")
async def startup_event():
    """Event handler for application startup."""
    print("Application starting up...")
    await create_db_and_tables() # Ensure database tables are created
    print("Database tables ensured.")

@app.on_event("shutdown")
async def shutdown_event():
    """Event handler for application shutdown."""
    print("Application shutting down...")
    pubsub_client.close()
    print("PubSubClient closed.")

# --- Root Endpoint ---
@app.get("/", summary="Root endpoint for API health check")
async def read_root():
    """
    Returns a simple message to indicate the API is running.
    """
    return {"message": "My Health Backend API is running!"}

# --- User Endpoints ---

@app.post("/users/register", response_model=User, status_code=status.HTTP_201_CREATED, summary="Register a new user")
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Registers a new user with the provided username, email, and password.
    Returns the newly created user object (excluding the hashed password).
    """
    new_user = await user_service.register_user(user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )
    return new_user

@app.post("/users/login", response_model=User, summary="Authenticate and log in a user")
async def login_user(
    username: str,
    password: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Authenticates a user with username and password.
    Returns the user object if authentication is successful.
    """
    user = await user_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user

@app.get("/users/{user_id}", response_model=User, summary="Get user details by ID")
async def get_user_details(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """
    Retrieves a user's details by their ID.
    """
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# --- Message Endpoints ---

@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED, summary="Send a new message")
async def send_message(
    message_data: MessageCreate,
    message_service: MessageService = Depends(get_message_service)
):
    """
    Sends a new message.
    The message will be saved to the database and published to Pub/Sub.
    """
    new_message = await message_service.create_and_publish_message(message_data)
    if not new_message:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message or publish to Pub/Sub."
        )
    # Broadcast the new message via WebSocket to relevant users (sender/receiver)
    await websocket_manager.send_to_user(message_data.sender_id, "new_message", new_message.model_dump())
    if message_data.receiver_id:
        await websocket_manager.send_to_user(message_data.receiver_id, "new_message", new_message.model_dump())
    return new_message

@app.get("/messages/user/{user_id}", response_model=List[Message], summary="Get all messages for a user")
async def get_messages_for_user(
    user_id: str,
    message_service: MessageService = Depends(get_message_service)
):
    """
    Retrieves all messages involving a specific user (sent or received).
    """
    messages = await message_service.get_user_messages(user_id)
    return messages

@app.get("/messages/conversation/{user1_id}/{user2_id}", response_model=List[Message], summary="Get conversation between two users")
async def get_conversation(
    user1_id: str,
    user2_id: str,
    message_service: MessageService = Depends(get_message_service)
):
    """
    Retrieves all direct messages exchanged between two specific users.
    """
    conversation = await message_service.get_message_conversation(user1_id, user2_id)
    return conversation

@app.put("/messages/{message_id}/read", response_model=Message, summary="Mark a message as read")
async def mark_message_as_read(
    message_id: str,
    message_service: MessageService = Depends(get_message_service)
):
    """
    Marks a specific message as read.
    """
    updated_message = await message_service.mark_message_as_read(message_id)
    if not updated_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return updated_message

# --- Questionnaire Endpoints ---

@app.post("/questionnaires", response_model=Questionnaire, status_code=status.HTTP_201_CREATED, summary="Create a new questionnaire")
async def create_questionnaire(
    q_data: QuestionnaireCreate,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Creates a new questionnaire with a title, description, and list of questions.
    """
    new_q = await q_service.create_questionnaire(q_data)
    if not new_q:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create questionnaire"
        )
    return new_q

@app.get("/questionnaires", response_model=List[Questionnaire], summary="Get all questionnaires")
async def get_all_questionnaires(
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Retrieves a list of all available questionnaires.
    """
    questionnaires = await q_service.get_all_questionnaires()
    return questionnaires

@app.get("/questionnaires/{q_id}", response_model=Questionnaire, summary="Get questionnaire by ID")
async def get_questionnaire_by_id(
    q_id: str,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Retrieves a specific questionnaire by its ID.
    """
    questionnaire = await q_service.get_questionnaire(q_id)
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    return questionnaire

@app.post("/questionnaire_sessions", response_model=QuestionnaireSession, status_code=status.HTTP_201_CREATED, summary="Start a new questionnaire session")
async def start_questionnaire_session(
    session_data: QuestionnaireSessionCreate,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Starts a new questionnaire session for a given user and questionnaire.
    """
    new_session = await q_service.start_questionnaire_session(session_data)
    if not new_session:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start questionnaire session"
        )
    return new_session

@app.post("/answers", response_model=Answer, status_code=status.HTTP_201_CREATED, summary="Submit an answer to a questionnaire session")
async def submit_answer(
    answer_data: AnswerCreate,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Submits an answer to a specific question within a questionnaire session.
    The answer will be saved to the database and published to Pub/Sub.
    """
    new_answer = await q_service.submit_answer(answer_data)
    if not new_answer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit answer or publish to Pub/Sub."
        )
    # Optionally broadcast answer (e.g., to a dashboard)
    # await websocket_manager.broadcast_message("new_answer", new_answer.model_dump())
    return new_answer

@app.get("/questionnaire_sessions/{session_id}/answers", response_model=List[Answer], summary="Get all answers for a session")
async def get_answers_for_session(
    session_id: str,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Retrieves all answers submitted for a specific questionnaire session.
    """
    answers = await q_service.get_session_answers(session_id)
    return answers

@app.put("/questionnaire_sessions/{session_id}/complete", response_model=QuestionnaireSession, summary="Mark a questionnaire session as complete")
async def complete_questionnaire_session(
    session_id: str,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Marks a questionnaire session as completed.
    """
    completed_session = await q_service.complete_session(session_id)
    if not completed_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire session not found"
        )
    return completed_session

@app.get("/users/{user_id}/questionnaire_sessions", response_model=List[QuestionnaireSession], summary="Get all questionnaire sessions for a user")
async def get_user_questionnaire_sessions(
    user_id: str,
    q_service: QuestionnaireService = Depends(get_questionnaire_service)
):
    """
    Retrieves all questionnaire sessions associated with a specific user.
    """
    sessions = await q_service.get_user_sessions(user_id)
    return sessions

# --- Clinical Insight Endpoints ---

@app.post("/clinical_insights", response_model=ClinicalInsight, status_code=status.HTTP_201_CREATED, summary="Create a new clinical insight")
async def create_clinical_insight(
    insight_data: ClinicalInsightCreate,
    insight_service: InsightService = Depends(get_insight_service)
):
    """
    Creates a new clinical insight. This endpoint might be used by agents
    or other backend processes to log insights directly.
    """
    new_insight = await insight_service.create_clinical_insight(insight_data)
    if not new_insight:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create clinical insight or publish to Pub/Sub."
        )
    # Potentially broadcast new insights to relevant parties (e.g., doctors dashboard)
    # await websocket_manager.broadcast_message("new_clinical_insight_for_dashboard", new_insight.model_dump())
    return new_insight

@app.get("/users/{user_id}/clinical_insights", response_model=List[ClinicalInsight], summary="Get clinical insights for a user")
async def get_clinical_insights_for_user(
    user_id: str,
    insight_service: InsightService = Depends(get_insight_service)
):
    """
    Retrieves all clinical insights associated with a specific user.
    """
    insights = await insight_service.get_user_insights(user_id)
    return insights

@app.get("/clinical_insights/{insight_id}", response_model=ClinicalInsight, summary="Get clinical insight by ID")
async def get_clinical_insight_by_id(
    insight_id: str,
    insight_service: InsightService = Depends(get_insight_service)
):
    """
    Retrieves a single clinical insight by its ID.
    """
    insight = await insight_service.get_insight(insight_id)
    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clinical insight not found"
        )
    return insight

# Example of an endpoint that might trigger an AI analysis (can also be an agent)
@app.post("/analyze_message_for_insight/{message_id}", summary="Trigger AI analysis for a message")
async def analyze_message_for_insight(
    message_id: str,
    message_service: MessageService = Depends(get_message_service),
    insight_service: InsightService = Depends(get_insight_service),
):
    """
    Triggers an AI analysis for a specific message and generates a clinical insight.
    (This is an example endpoint; usually, agents would do this on Pub/Sub events).
    """
    message = await message_service.message_repo.get_message_by_id(message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    # Generate insight using AI
    generated_text = await insight_service.generate_insight_with_ai(
        message.sender_id,
        message.content,
        "manual_message_analysis",
        message.id
    )

    # Create and store the insight
    insight_create_data = ClinicalInsightCreate(
        user_id=message.sender_id,
        source_type="manual_message_analysis",
        source_id=message.id,
        insight_text=generated_text,
        severity="medium", # This would ideally come from AI analysis
        recommendations="Review message context."
    )
    new_insight = await insight_service.create_clinical_insight(insight_create_data)

    if not new_insight:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate or store insight."
        )

    return {"message": "Insight generated and stored", "insight_id": new_insight.id}

