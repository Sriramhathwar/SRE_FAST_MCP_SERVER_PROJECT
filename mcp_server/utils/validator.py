def validate_promql(q):
    blocked = ["delete", "drop", "shutdown"]
    return not any(b in q.lower() for b in blocked)