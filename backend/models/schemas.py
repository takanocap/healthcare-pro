from pydantic import BaseModel
from typing import Optional

class MessageRequest(BaseModel):
    message: str
    patientId: str
    

class MessageResponse(BaseModel):
    reply: str


class QuestionnaireTrigger(BaseModel):
    patientId: str
    reason: str


class MonitorTrigger(BaseModel):
    patientId: Optional[str] = None


class AlertPayload(BaseModel):
    patientId: str
    riskScore: str
    summary: str