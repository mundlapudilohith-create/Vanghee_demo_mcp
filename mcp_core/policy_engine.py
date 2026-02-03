def apply_policy(intent_def, user_role):
    if user_role not in intent_def.get("allowed_roles", []):
        raise PermissionError("Role not allowed for this intent")

    if intent_def.get("approval_required"):
        return "REQUIRES_APPROVAL"

    return "AUTO"

