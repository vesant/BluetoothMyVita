import logging
import socket
from typing import Tuple

from .base import TransportServer
from ..protocol.parser import parse_event_line

logger = logging.getLogger(__name__)


class TcpTransportServer(TransportServer):
    def __init__(self, host: str, port: int, on_event):
        super().__init__(on_event)
        self._host = host
        self._port = port

    def serve_forever(self) -> None:
        address: Tuple[str, int] = (self._host, self._port)
        logger.info("TCP server listening on %s:%s", self._host, self._port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(address)
            server.listen(1)

            while True:
                client, remote = server.accept()
                logger.info("Client connected: %s:%s", remote[0], remote[1])
                with client:
                    for raw in client.makefile("r", encoding="utf-8"):
                        line = raw.strip()
                        if not line:
                            continue
                        try:
                            event = parse_event_line(line)
                            self._on_event(event)
                        except Exception:
                            logger.exception("Failed to parse event: %s", line)
                logger.info("Client disconnected")
