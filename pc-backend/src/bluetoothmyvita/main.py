import argparse
import logging

from .config import Config
from .controller.directinput_emulator import DirectInputEmulator
from .logging_utils import configure_logging
from .transport.bluetooth_server import BluetoothTransportServer
from .transport.tcp_server import TcpTransportServer

logger = logging.getLogger(__name__)


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description="BluetoothMyVita PC backend")
    parser.add_argument("--transport", default="bluetooth", choices=["bluetooth", "tcp"])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=1977)
    parser.add_argument("--log-level", default="info")
    args = parser.parse_args()

    configure_logging(args.log_level)
    return Config(transport=args.transport, host=args.host, port=args.port)


def main() -> None:
    config = parse_args()
    emulator = DirectInputEmulator()

    def on_event(event):
        emulator.apply_event(event)

    if config.transport == "tcp":
        server = TcpTransportServer(config.host, config.port, on_event)
    else:
        server = BluetoothTransportServer(on_event)

    try:
        server.serve_forever()
    except NotImplementedError as exc:
        logger.error(str(exc))


if __name__ == "__main__":
    main()
