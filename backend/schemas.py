# backend/schemas.py

from pydantic import BaseModel

# For /chat endpoint
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# For /book endpoint
class BookingRequest(BaseModel):
    start: str  # ISO 8601 format e.g., "2025-07-03T15:00:00+05:30"
    end: str
    summary: str

class BookingResponse(BaseModel):
    success: bool
    event_link: str
