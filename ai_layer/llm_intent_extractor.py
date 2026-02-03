# ai_layer/llm_intent_extractor.py
import requests, json, re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2:0.5b"

def extract_intent(text: str):
    prompt = f"""
You are an intent extractor for a GST assistant.

Return JSON ONLY:
{{
  "intent": "calculate_gst | check_gstin_status | calculate_late_fee | generate_gst_report | unknown",
  "confidence": 0.0-1.0,
  "entities": {{
    "amount": number | null,
    "gst_rate": number | null,
    "gstin": string | null,
    "delay_days": number | null
  }}
}}

User input:
{text}
"""

    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=20)

        raw = r.json()["response"]
        return json.loads(raw)

    except Exception:
        # fallback extractor
        amount_match = re.search(r"(\d+(\.\d+)?)", text)
        amount = float(amount_match.group(1)) if amount_match else None

        return {
            "intent": "calculate_gst" if "gst" in text.lower() else "unknown",
            "confidence": 0.7 if amount else 0.0,
            "entities": {
                "amount": amount,
                "gst_rate": 18
            }
        }
