from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    BUTTON = "button"
    AXIS = "axis"
    HAT = "hat"


class ButtonAction(str, Enum):
    PRESS = "press"
    RELEASE = "release"


@dataclass
class InputEvent:
    event_type: EventType
    control: str
    value: float
    action: Optional[ButtonAction] = None
