from models.schemas import MonitorTrigger
from services.data import get_patient_time_series
from agents.alert import send_alert
from fastapi import HTTPException


def analyze_patient_trends(trigger: MonitorTrigger) -> dict:
    patient_id = trigger.patientId
    data = get_patient_time_series(patient_id)
    if not data:
        raise HTTPException(status_code=404, detail="Patient data not found")
    
    alerts = []
    for patient in data:
        risk = sum(pt['score'] for pt in patient['points']) / len(patient['points'])
        if risk > 0.7:
            alerts.append(send_alert({
                "patientId": patient['id'],
                "riskScore": str(risk),
                "summary": f"Patient {patient_id} has a high risk score of {risk:.2f}. Immediate attention required."
            }))
    return {"alerts": alerts, "analyzed": len(data), "alerts_sent": len(alerts)} if alerts else {"message": "No significant negative trends detected."}