from models.schemas import AlertPayload


def send_alert(payload: dict) -> dict:
    print(f"Alert sent for patient {payload['patientId']}: {payload['summary']} (Risk Score: {payload['riskScore']})")
    return {
        "status": "sent",
        "patientId": payload['patientId'],
        "risk": payload['riskScore'],
        "message": f"Alert sent for patient {payload['patientId']}"
    }