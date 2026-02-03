from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

from ai_layer.llm_intent_extractor import extract_intent
from ai_layer.ai_orchestrator import handle_ai_response

API_KEY = "vanghee-dev-key"
MCP_ROUTE_URL = "https://miniature-invention-5gp7jr4jj4xvf664-7001.app.github.dev/"

app = FastAPI(title="Vanghee AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str
    user_role: str = "user"

@app.post("/mcp/llm_extract")
def llm_extract(req: UserInput, x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 1️⃣ Extract intent from LLM
    ai_result = extract_intent(req.text)

    # 2️⃣ Send to MCP gateway
    mcp_response = handle_ai_response(ai_result, user_role=req.user_role)

    return mcp_response

@app.get("/health")
def health():
    return {"status": "ok"}
