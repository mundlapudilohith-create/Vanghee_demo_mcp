import json
from mcp_core.router import route_intent

def run():
    # ---- INPUT (simulating AI output) ----
    ai_result = {
        "intent": "calculate_gst",
        "confidence": 0.87,
        "entities": {
            "amount": 1000,
            "gst_rate": 18
        }
    }

    user_role = "USER"

    # ---- MCP ROUTE ----
    response = route_intent(
        intent=ai_result["intent"],
        user_role="admin",
        payload=ai_result["entities"]
    )

    # ---- JSON OUTPUT ----
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    run()
