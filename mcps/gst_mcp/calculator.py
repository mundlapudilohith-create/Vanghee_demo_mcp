def calculate_gst(entities: dict):
    raw_amount = entities.get("amount")
    raw_gst_rate = entities.get("gst_rate", 18)

    if raw_amount is None:
        return {"status": "FAILED", "reason": "AMOUNT_REQUIRED"}

    # ✅ Safe casting (LLM may send strings)
    try:
        amount = float(raw_amount)
        gst_rate = float(raw_gst_rate)
    except Exception:
        return {
            "status": "FAILED",
            "reason": "INVALID_AMOUNT_OR_GST_RATE",
            "detail": {
                "amount": raw_amount,
                "gst_rate": raw_gst_rate
            }
        }

    gst = amount * gst_rate / 100

    return {
        "status": "SUCCESS",
        "data": {
            "amount": amount,
            "gst_rate": gst_rate,
            "gst": gst,
            "total": amount + gst
        }
    }


def calculate_gst_interest(entities: dict):
    gstin = entities.get("gstin", "UNKNOWN")
    return {"status": "SUCCESS", "data": {"gstin": gstin, "interest": 180}}


def check_gstin_status(entities: dict):
    gstin = entities.get("gstin", "UNKNOWN")
    valid = gstin.startswith("27") and len(gstin) == 15  # Dummy validation
    return {"status": "SUCCESS", "data": {"gstin": gstin, "valid": valid}}


def calculate_late_fee(entities: dict):
    raw_tax_amount = entities.get("tax_amount", 0)
    raw_delay_days = entities.get("delay_days", 0)

    try:
        tax_amount = float(raw_tax_amount)
        delay_days = int(raw_delay_days)
    except Exception:
        return {
            "status": "FAILED",
            "reason": "INVALID_LATE_FEE_INPUT",
            "detail": {
                "tax_amount": raw_tax_amount,
                "delay_days": raw_delay_days
            }
        }

    late_fee = tax_amount * 0.001 * delay_days
    return {"status": "SUCCESS", "data": {"tax_amount": tax_amount, "delay_days": delay_days, "late_fee": late_fee}}


def generate_gst_report(entities: dict):
    from_date = entities.get("from_date", "2026-01-01")
    to_date = entities.get("to_date", "2026-01-31")
    report = {"total_tax": 10000}  # Dummy report
    return {"status": "SUCCESS", "data": {"from_date": from_date, "to_date": to_date, "report": report}}


def file_gst_return(entities: dict):
    month = entities.get("month", "01")
    year = entities.get("year", 2026)
    return_id = f"GST{year}{month}001"
    return {"status": "SUCCESS", "data": {"return_id": return_id}}


def reconcile_gst_payment(entities: dict):
    invoice_ids = entities.get("invoice_ids", [])
    gstin = entities.get("gstin", "UNKNOWN")
    result = {"matched": len(invoice_ids)}
    return {"status": "SUCCESS", "data": {"gstin": gstin, "reconciliation": result}}


def generate_e_way_bill(entities: dict):
    gstin = entities.get("gstin", "UNKNOWN")
    invoice_id = entities.get("invoice_id", "INV001")
    transport_mode = entities.get("transport_mode", "Road")
    e_way_bill_id = f"EWB-{invoice_id}"
    return {
        "status": "SUCCESS",
        "data": {
            "gstin": gstin,
            "invoice_id": invoice_id,
            "transport_mode": transport_mode,
            "e_way_bill_id": e_way_bill_id
        }
    }


def validate_invoice(entities: dict):
    invoice_id = entities.get("invoice_id", "INV001")
    gstin = entities.get("gstin", "UNKNOWN")
    return {"status": "SUCCESS", "data": {"invoice_id": invoice_id, "gstin": gstin, "valid": True}}


def track_gst_payment(entities: dict):
    gstin = entities.get("gstin", "UNKNOWN")
    period = entities.get("period", "2026-01")
    status = "PAID"  # Dummy status
    return {"status": "SUCCESS", "data": {"gstin": gstin, "period": period, "payment_status": status}}


def cancel_gst_return(entities: dict):
    return_id = entities.get("return_id", "UNKNOWN")
    reason = entities.get("reason", "No reason provided")
    return {
        "status": "SUCCESS",
        "data": {
            "return_id": return_id,
            "cancelled": True,
            "reason": reason
        }
    }
