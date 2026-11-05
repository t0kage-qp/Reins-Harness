MAX_MESSAGES = 20

def _role(m) -> str:
    """History may hold dicts or SDK message objects."""
    return m["role"] if isinstance(m, dict) else m.role


def trim_history(messages: list, limit: int = MAX_MESSAGES) -> list:
    """Return a trimmed copy: system message + latest messages,
    starting at a user message so tool_calls/tool pairs are never split."""
    head = messages[:1] if messages and _role(messages[0]) == "system" else []
    rest = messages[len(head):]
    if len(rest) <= limit:
        return messages[:]
    start = len(rest) - limit
    while start < len(rest) and _role(rest[start]) != "user":
        start += 1
    if start == len(rest):  # no user message in the window: use the last one
        start = max(i for i, m in enumerate(rest) if _role(m) == "user")
    return head + rest[start:]