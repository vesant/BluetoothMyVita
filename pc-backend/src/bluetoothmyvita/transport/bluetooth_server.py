import asyncio
import logging
from typing import List

from .base import TransportServer

logger = logging.getLogger(__name__)


class BluetoothTransportServer(TransportServer):
    def __init__(self, on_event):
        super().__init__(on_event)

    def serve_forever(self) -> None:
        try:
            asyncio.run(self._scan_and_select())
        except KeyboardInterrupt:
            logger.info("Encerrado pelo utilizador")

    async def _scan_and_select(self) -> None:
        try:
            from bleak import BleakClient, BleakScanner
        except Exception as exc:
            raise NotImplementedError(
                "Bluetooth BLE requer a dependencia 'bleak'. "
                "Instala com: pip install bleak"
            ) from exc

        while True:
            devices = await BleakScanner.discover(timeout=5.0)
            if not devices:
                print("Nenhum dispositivo BLE encontrado. A tentar novamente...")
                continue

            self._print_devices(devices)
            choice = self._prompt_choice(len(devices))
            if choice is None:
                continue

            device = devices[choice]
            name = (device.name or "").strip()
            if not self._confirm_psvita(name, device.address):
                print("Nao escolheu uma PSVita. Escolha outro dispositivo.")
                continue

            print("A tentar ligar a %s (%s)..." % (device.name, device.address))
            async with BleakClient(device) as client:
                if not client.is_connected:
                    print("Falha ao ligar ao dispositivo.")
                    continue

                try:
                    await client.get_services()
                except Exception:
                    logger.exception("Falha ao obter informacao do dispositivo")
                    print("Ligado, mas nao foi possivel obter informacao.")
                    return

                print("Ligacao confirmada. Dispositivo ativo: %s" % device.name)
                return

    @staticmethod
    def _print_devices(devices: List[object]) -> None:
        print("\nDispositivos BLE encontrados:")
        print("ID  Nome                             Endereco           RSSI")
        print("--  -------------------------------  -----------------  ----")
        for idx, device in enumerate(devices, start=1):
            name = device.name or "(sem nome)"
            rssi = getattr(device, "rssi", None)
            rssi_text = str(rssi) if rssi is not None else "?"
            print("%2d  %-31s  %-17s  %4s" % (idx, name[:31], device.address, rssi_text))

    @staticmethod
    def _prompt_choice(total: int):
        while True:
            raw = input("Escolhe um ID (ou 'r' para voltar a procurar): ").strip().lower()
            if raw == "r":
                return None
            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= total:
                    return idx - 1
            print("Opcao invalida.")

    @staticmethod
    def _confirm_psvita(name: str, address: str) -> bool:
        lower = name.lower()
        if "vita" in lower or "psvita" in lower:
            return True
        print("Dispositivo sem nome ou sem 'vita': %s (%s)" % (name or "(sem nome)", address))
        raw = input("Confirmas que este e a PSVita? (s/n): ").strip().lower()
        return raw in {"s", "sim", "y", "yes"}
