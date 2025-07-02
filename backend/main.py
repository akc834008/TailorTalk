# backend/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent
from backend.schemas import ChatRequest, ChatResponse

# ✅ Ensure credential.json is available at runtime (for Render Secret File support)
os.makedirs("config", exist_ok=True)
if os.path.exists("/etc/secrets/credential_json"):
    with open("/etc/secrets/credential_json", "r") as src:
        with open("config/credential.json", "w") as dst:
            dst.write(src.read())

# ✅ Declare FastAPI app at top level
app = FastAPI()

# ✅ Allow frontend access (CORS config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to frontend origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route for health check or browser access
@app.get("/")
def root():
    return {"message": "✅ TailorTalk backend is live! Use POST /chat with JSON."}

# ✅ Chat endpoint for LangChain agent
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message
    llm_response = run_agent(user_message)
    return ChatResponse(response=llm_response)
