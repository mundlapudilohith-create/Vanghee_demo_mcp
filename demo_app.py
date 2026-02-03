from ai_layer.llm_intent_extractor import extract_intent
from mcp_core.router import route_intent

user_input = "I didn’t pay my GST this month. Calculate interest."

llm_result = extract_intent(user_input)

intent = llm_result["intent"]
entities = llm_result["entities"]

response = route_intent(
    intent=intent,
    user_role="ai_agent",
    payload={
        "gstin": entities.get("gstin", "29ABCDE1234F1Z5"),
        "period": entities.get("period", "2024-12")
    }
)
llm_result = extract_intent(user_input)

if llm_result["intent"] == "unknown":
    print({
        "status": "REJECTED",
        "reason": "INTENT_UNKNOWN",
        "ai_result": llm_result
    })
print("\nFINAL RESPONSE:")
print("LLM RESULT:", llm_result)
print(response)
