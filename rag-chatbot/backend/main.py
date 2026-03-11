import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel import Session
from typing import Optional
from models import Conversation, Message
from database import get_session
from tools.todo_tools import TodoTools
from agents.todo_agent import TodoAIAssistant
from pydantic import BaseModel
#from auth import auth_handler
from datetime import datetime

app = FastAPI(title="Todo AI Chatbot API")


# ========================
# Request / Response Models
# ========================
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    timestamp: datetime


# ========================
# Chat Endpoint
# ========================
@app.post("/api/{user_id}/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_session)
):
    # ------------------------
    # AUTH (Safe Handling)
    # ------------------------
    token_user_id = user_id  # default for testing

    if authorization:
        try:
            token = authorization.replace("Bearer ", "")
            token_user_id = auth_handler.verify_token(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    # Check user access
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # ------------------------
    # Get or Create Conversation
    # ------------------------
    conversation = None

    if request.conversation_id:
        conversation = db.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # ------------------------
    # Save User Message
    # ------------------------
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # ------------------------
    # Initialize Tools + AI
    # ------------------------
    tools = TodoTools(db, user_id)
    ai_assistant = TodoAIAssistant(tools)

    # AI Response
    try:
        response_text = ai_assistant.process_message(request.message)
    except Exception as e:
        response_text = f"AI Error: {str(e)}"

    # ------------------------
    # Save Assistant Message
    # ------------------------
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=response_text
    )
    db.add(assistant_message)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        timestamp=datetime.utcnow()
    )


# ========================
# Root Test Endpoint
# ========================
@app.get("/")
def read_root():
    return {"message": "Backend is running successfully"}
