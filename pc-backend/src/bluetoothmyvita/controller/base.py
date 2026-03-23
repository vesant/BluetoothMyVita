from abc import ABC, abstractmethod

from ..protocol.models import InputEvent


class ControllerEmulator(ABC):
    @abstractmethod
    def apply_event(self, event: InputEvent) -> None:
        raise NotImplementedError
