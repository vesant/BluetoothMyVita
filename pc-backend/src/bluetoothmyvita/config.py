from dataclasses import dataclass


@dataclass
class Config:
    transport: str = "bluetooth"
    host: str = "0.0.0.0"
    port: int = 1977
