from mcp_core.intent_loader import load_intents
from mcp_core.policy_engine import apply_policy
from mcp_core.audit_logger import audit_log
from mcp_core.schema_validator import validate_schema
from mcps.gst_mcp.handler import handle as gst_handler

INTENT_REGISTRY = load_intents("registry")

MCP_CLIENTS = {
    "gst_mcp": gst_handler
}

def route_intent(intent: str, user_role: str, payload: dict):

    # 1️⃣ Intent existence check
    if intent not in INTENT_REGISTRY:
        return {
            "status": "REJECTED",
            "reason": "INTENT_NOT_REGISTERED",
            "intent": intent,
            "message": "This request is not supported yet."
        }

    intent_def = INTENT_REGISTRY[intent]
     # ✅ Schema validation
     
    schema_result = validate_schema(intent_def, payload)
    if schema_result["status"] != "SUCCESS":
        return schema_result

    # 2️⃣ Apply policy safely
    policy = apply_policy(intent_def, user_role)

    audit_log({
        "intent": intent,
        "role": user_role,
        "policy": policy
    })

    # 3️⃣ Policy gate
    if policy.get("status") != "AUTO":
        return {
            "status": "REJECTED",
            "reason": "POLICY_BLOCKED",
            "policy": policy
        }

    # 4️⃣ Route to MCP handler
    mcp_name = intent_def["mcp"]
    handler = MCP_CLIENTS.get(mcp_name)

    if not handler:
        return {
            "status": "ERROR",
            "reason": "MCP_NOT_FOUND",
            "mcp": mcp_name
        }

    # 5️⃣ Call MCP handler (PASS INTENT + PAYLOAD)
    result = handler(intent, payload)

    return {
        "status": "SUCCESS",
        "reason": None,
        "data": result
    }
