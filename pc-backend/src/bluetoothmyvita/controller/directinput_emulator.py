import logging

from .base import ControllerEmulator
from ..protocol.models import InputEvent

logger = logging.getLogger(__name__)


class DirectInputEmulator(ControllerEmulator):
    def apply_event(self, event: InputEvent) -> None:
        logger.info("DirectInput placeholder: %s", event)
