# main.py
import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.agents.orchestrator import HealthcarePROOrchestrator
from app.database import SessionLocal, engine, Base
from app.models.models import User
from app.schemas.schemas import UserLogin, UserResponse
from pydantic import BaseModel
from typing import Optional


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Healthcare PRO Multi-Agent System")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = HealthcarePROOrchestrator()


class PatientInteractionRequest(BaseModel):
    """Schema of patient request body"""
    patient_id: str
    interaction_type: str  # "checkin", "questionnaire", "trend_analysis"
    patient_data: dict
    user_message: Optional[str] = None


class PatientInteractionResponse(BaseModel):
    """Schema of patient response body"""
    agent_response: dict
    next_action: Optional[str] = None
    metadata: Optional[dict] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login endpoint"""
    existing_user = db.query(User).filter_by(
        username=user.username,
        date_of_birth=user.date_of_birth
    ).first()

    if existing_user:
        return UserResponse(
            id=existing_user.id,
            username=existing_user.username,
            date_of_birth=existing_user.date_of_birth,
            condition="Hypertension",  # Dummy condition
            language="English"
        )

    new_user = User(username=user.username, date_of_birth=user.date_of_birth)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        date_of_birth=new_user.date_of_birth,
        condition="Hypertension",  # Dummy condition
        language="English"
    )


@app.post("/api/agent/interact", response_model=PatientInteractionResponse)
async def interact_with_agent(request: PatientInteractionRequest):
    """Main endpoint for agent interactions"""
    try:
        print("Received request:", request.model_dump_json)
        response = await orchestrator.handle_patient_interaction(
            request.patient_data,
            request.interaction_type,
            request.user_message
        )
        return PatientInteractionResponse(
            agent_response=response,
            next_action=response.get("next_action"),
            metadata={"timestamp": datetime.datetime.now().isoformat()}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agents": "ready"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
