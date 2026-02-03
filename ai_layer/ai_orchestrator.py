# ai_layer/ai_orchestrator.py
import requests

MCP_ROUTE_URL = "https://miniature-invention-5gp7jr4jj4xvf664-7001.app.github.dev/mcp/route"
API_KEY = "vanghee-dev-key"
CONFIDENCE_THRESHOLD = 0.5

def handle_ai_response(ai_response: dict, user_role="user"):
    intent = ai_response.get("intent")
    confidence = ai_response.get("confidence", 0)
    entities = ai_response.get("entities", {})

    if not intent:
        return {"status": "REJECTED", "reason": "INTENT_MISSING"}

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "status": "REJECTED",
            "reason": "LOW_CONFIDENCE",
            "confidence": confidence
        }

    payload = {
        "intent": intent,
        "user_role": user_role,
        "payload": entities
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    resp = requests.post(MCP_ROUTE_URL, json=payload, headers=headers, timeout=10)

    print("🔁 MCP STATUS:", resp.status_code)
    print("🔁 MCP RAW RESPONSE:", resp.text)

    try:
        return resp.json()
    except Exception:
        return {
            "status": "ERROR",
            "reason": "MCP_INVALID_RESPONSE",
            "raw_response": resp.text
        }


