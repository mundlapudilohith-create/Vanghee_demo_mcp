import requests

MCP_URL = "http://localhost:8001/mcp/route"
API_KEY = "vanghee-dev-key"

CONFIDENCE_THRESHOLD = 0.6

def handle_ai_response_http(ai_response: dict, user_role="ai_agent"):
    intent = ai_response.get("intent")
    confidence = ai_response.get("confidence", 0)
    entities = ai_response.get("entities", {})

    if not intent:
        return {"status": "REJECTED", "reason": "INTENT_MISSING"}

    if confidence < CONFIDENCE_THRESHOLD:
        return {"status": "REJECTED", "reason": "LOW_CONFIDENCE", "confidence": confidence}

    resp = requests.post(
        MCP_URL,
        headers={"X-API-Key": API_KEY},
        json={
            "intent": intent,
            "user_role": user_role,
            "payload": entities
        },
        timeout=30
    )

    return resp.json()
