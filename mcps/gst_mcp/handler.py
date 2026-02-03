from typing import Dict, Any
from . import calculator
import database.gst_operations as db_ops


def handle(intent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if intent == "calculate_gst":
            result = calculator.calculate_gst(payload)

            if result.get("status") == "SUCCESS":
                gst_data = result.get("data", {})

                try:
                    db_ops.save_gst_transaction(
                        gstin=payload.get("gstin", "UNKNOWN"),
                        amount=gst_data.get("amount"),
                        gst_rate=gst_data.get("gst_rate"),
                        gst_amount=gst_data.get("gst"),
                        total_amount=gst_data.get("total")
                    )
                except Exception as db_err:
                    print("⚠️ DB save failed:", db_err)

            return result   # MCP returns domain result

        elif intent == "check_gstin_status":
            return calculator.check_gstin_status(payload)

        elif intent == "calculate_late_fee":
            return calculator.calculate_late_fee(payload)

        elif intent == "generate_gst_report":
            return calculator.generate_gst_report(payload)

        elif intent == "file_gst_return":
            return calculator.file_gst_return(payload)

        elif intent == "reconcile_gst_payment":
            return calculator.reconcile_gst_payment(payload)

        elif intent == "generate_e_way_bill":
            return calculator.generate_e_way_bill(payload)

        elif intent == "validate_invoice":
            return calculator.validate_invoice(payload)

        elif intent == "track_gst_payment":
            return calculator.track_gst_payment(payload)

        elif intent == "cancel_gst_return":
            return calculator.cancel_gst_return(payload)

        elif intent == "calculate_gst_interest":
            return calculator.calculate_gst_interest(payload)

        else:
            return {
                "status": "REJECTED",
                "reason": "INTENT_NOT_IMPLEMENTED",
                "intent": intent
            }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": "GST MCP internal error",
            "detail": str(e)
        }

