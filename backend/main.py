from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import (
    QuestionnaireTrigger, MessageResponse, MonitorTrigger, 
    MessageRequest, AlertPayload
)
from agents import companion, questionnaire, monitor, alert
import os

app = FastAPI(
    title="Healthcare Pro API",
    description="API for Healthcare Pro, a healthcare companion application.",
    version="1.0.0"
)

# CORS configuration
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare Pro API!"}

@app.post("/api/v1/companion/respond", response_model=MessageResponse)
def companion_respond(req: MessageRequest):
    return companion.respond_to_patient(req)

@app.post("/api/v1/questionnaire/start", response_model=MessageResponse)
def start_questionnaire(trigger: QuestionnaireTrigger):
    return questionnaire.start_questionnaire(trigger)

@app.post("/api/v1/monitor/analyze", response_model=dict)
def analyze_trends(trigger: MonitorTrigger):
    return monitor.analyze_patient_trends(trigger)

@app.post("/api/v1/alert/send", response_model=dict)
def send_alert_directly(payload: AlertPayload):
    return alert.send_alert(payload.dict())
