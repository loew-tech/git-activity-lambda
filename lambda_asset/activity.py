def sanitize_event(event: dict) -> dict:
    if event["public"]:
        return {
            "type": event["type"],
            "repository": event["repo"]["name"],
            "public": True,
            "timestamp": event["created_at"],
        }

    return {
        "type": event["type"],
        "public": False,
        "timestamp": event["created_at"],
    }