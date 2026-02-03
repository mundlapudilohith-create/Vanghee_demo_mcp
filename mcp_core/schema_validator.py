def validate_schema(intent_def: dict, payload: dict):
    schema = intent_def.get("schema", {})

    errors = []

    for field, field_type in schema.items():
        if field not in payload:
            errors.append(f"Missing field: {field}")
            continue

        value = payload.get(field)

        if field_type == "number":
            try:
                float(value)
            except Exception:
                errors.append(f"Field '{field}' must be number, got {value}")

        elif field_type == "string":
            if not isinstance(value, str):
                errors.append(f"Field '{field}' must be string, got {type(value)}")

        elif field_type == "list":
            if not isinstance(value, list):
                errors.append(f"Field '{field}' must be list, got {type(value)}")

    if errors:
        return {
            "status": "FAILED",
            "reason": "SCHEMA_VALIDATION_FAILED",
            "errors": errors
        }

    return {"status": "SUCCESS"}
