from models.schemas import MessageRequest, MessageResponse


def respond_to_patient(req: MessageRequest) -> MessageResponse:
    reply = (
        "Hello! I'm your healthcare companion. How are you doing today?"
        if "tired" in req.message.lower() or "sad" in req.message.lower()
        else "I'm here to assist you with any healthcare-related questions or concerns you may have. How can I help you today?"
    )
    return MessageResponse(reply=reply)