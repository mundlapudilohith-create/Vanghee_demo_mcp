from datetime import datetime

def audit_log(event):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        **event
    }
    print("AUDIT LOG:", log)

