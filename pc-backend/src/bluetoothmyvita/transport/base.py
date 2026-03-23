from abc import ABC, abstractmethod
from typing import Callable

from ..protocol.models import InputEvent


EventHandler = Callable[[InputEvent], None]


class TransportServer(ABC):
    def __init__(self, on_event: EventHandler) -> None:
        self._on_event = on_event

    @abstractmethod
    def serve_forever(self) -> None:
        raise NotImplementedError
