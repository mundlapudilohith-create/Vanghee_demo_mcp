from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, Optional

from mcp_core.router import route_intent
from ai_layer.llm_intent_extractor import extract_intent
from ai_layer.ai_orchestrator import handle_ai_response

API_KEY = "vanghee-dev-key"
app = FastAPI(title="Vanghee MCP Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str
    user_role: str = "user"

class MCPRequest(BaseModel):
    intent: str
    user_role: Optional[str] = "user"
    payload: Optional[Dict[str, Any]] = {}

class MCPResponse(BaseModel):
    status: str
    reason: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    ai_result: Optional[Dict[str, Any]] = None


# 🔹 LLM → MCP bridge
@app.post("/mcp/llm_extract")
def llm_extract(req: UserInput, x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    ai_result = extract_intent(req.text)

    if not ai_result:
        return JSONResponse(
            status_code=400,
            content={"status": "ERROR", "reason": "LLM_RETURNED_EMPTY"}
        )

    try:
        mcp_response = handle_ai_response(ai_result, user_role=req.user_role)
        return JSONResponse(content=mcp_response)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "reason": "MCP_INTERNAL_ERROR",
                "detail": str(e)
            }
        )


# 🔹 Direct MCP route (no LLM)
@app.post("/mcp/route", response_model=MCPResponse)
def mcp_route(
    req: MCPRequest,
    x_api_key: str = Header(..., alias="X-API-Key")  # enforce API key
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = route_intent(
            intent=req.intent,
            user_role=req.user_role,
            payload=req.payload
        )

        # 🔐 Always return JSON
        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "reason": "MCP_CRASH",
                "detail": str(e)
            }
        )


@app.get("/health")
def health():
    return {"status": "ok"}
