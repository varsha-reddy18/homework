from pydantic import BaseModel
from typing import Optional, List

# -----------------------
# USER QUESTION (CHAT)
# -----------------------
class Question(BaseModel):
    question: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    subject: Optional[str] = None


class AnswerResponse(BaseModel):
    answer: str
    session_id: Optional[str] = None


# -----------------------
# IMAGE OCR RESPONSE
# -----------------------
class ImageResponse(BaseModel):
    extracted_question: str
    answer: str
    user_id: Optional[str] = None


# -----------------------
# CHAT HISTORY
# -----------------------
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatHistory(BaseModel):
    session_id: str
    messages: List[ChatMessage]


# -----------------------
# STUDY PLAN REQUEST
# -----------------------
class StudyPlanRequest(BaseModel):
    topic: str
    days: int = 7
    hours_per_day: Optional[int] = 2
    difficulty: Optional[str] = "medium"
    subject: Optional[str] = "General"