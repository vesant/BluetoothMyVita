# PC Backend

Este backend recebe eventos da PSVita e emula um controller no Windows.

## Requisitos
- Python 3.10+

## Executar (teste local via TCP)
1) `python -m bluetoothmyvita --transport tcp`
2) Enviar eventos como linhas JSON para `localhost:1977`

Exemplo de evento:
```json
{"type":"button","control":"cross","action":"press","value":1}
```

## Estado
- Transporte Bluetooth: placeholder
- Emulacao DirectInput: placeholder (a implementar)
