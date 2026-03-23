import json
from typing import Any, Dict

from .models import ButtonAction, EventType, InputEvent


def parse_event_line(line: str) -> InputEvent:
    payload: Dict[str, Any] = json.loads(line)
    event_type = EventType(payload["type"])
    control = str(payload.get("control", ""))
    value = float(payload.get("value", 0))

    action = payload.get("action")
    button_action = ButtonAction(action) if action is not None else None

    return InputEvent(
        event_type=event_type,
        control=control,
        value=value,
        action=button_action,
    )
