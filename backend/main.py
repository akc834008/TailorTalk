# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent
from backend.schemas import ChatRequest, ChatResponse

# ✅ Declare FastAPI app at top level (required for uvicorn)
app = FastAPI()

# ✅ CORS config: allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Main /chat endpoint used by Streamlit
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message
    llm_response = run_agent(user_message)
    return ChatResponse(response=llm_response)
