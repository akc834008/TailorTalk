# backend/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent
from backend.schemas import ChatRequest, ChatResponse

# ✅ Copy secret file from /etc/secrets to expected path at startup
os.makedirs("config", exist_ok=True)
if os.path.exists("/etc/secrets/credential_json"):
    with open("/etc/secrets/credential_json", "r") as src:
        with open("config/credential.json", "w") as dst:
            dst.write(src.read())

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

# ✅ Health check route for GET /
@app.get("/")
def health_check():
    return {"message": "✅ TailorTalk backend is live!"}

# ✅ Main /chat endpoint used by Streamlit
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message
    llm_response = run_agent(user_message)
    return ChatResponse(response=llm_response)
