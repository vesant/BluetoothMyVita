from .base import TransportServer


class BluetoothTransportServer(TransportServer):
    def __init__(self, on_event):
        super().__init__(on_event)

    def serve_forever(self) -> None:
        raise NotImplementedError(
            "Bluetooth transport not implemented. "
            "Use --transport tcp for now."
        )
