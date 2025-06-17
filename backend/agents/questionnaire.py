from models.schemas import QuestionnaireTrigger, MessageResponse

QUESTIONS = [
    "How has your energy level been in the past week?",
    "Have you experienced any discomfort, pain or discomfort in your body?",
    "Have you taken your medications as prescribed?",
    "Have you had any changes in your appetite or weight?",
    "Have you had any trouble sleeping or changes in your sleep patterns?",
]


def start_questionnaire(trigger: QuestionnaireTrigger) -> MessageResponse:
    # """
    # Starts a questionnaire for the patient based on the trigger.
    # """
    patient_id = trigger.patientId
    reason = trigger.reason

    first_question = QUESTIONS[0]
    
    return MessageResponse(reply=f"Let's begin your check-in. {first_question}")