# backend/main.py

import os

# ✅ Step 1: Copy secret from /etc/secrets/ to config/ folder before anything else
os.makedirs("config", exist_ok=True)
secret_path = "/etc/secrets/credential_json"
target_path = "config/credential.json"
if os.path.exists(secret_path) and not os.path.exists(target_path):
    with open(secret_path, "r") as src, open(target_path, "w") as dst:
        dst.write(src.read())

# ✅ Step 2: Normal imports after credentials are placed
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.agent import run_agent
from backend.schemas import ChatRequest, ChatResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message
    llm_response = run_agent(user_message)
    return ChatResponse(response=llm_response)
