# BluetoothMyVita
Transforma a PSVita num controller para PC.

## Estrutura do projeto
- `pc-backend/`: backend no PC (processa eventos e emula controller)
- `psvita/`: espaco reservado para a app da PSVita

## Estado atual
- Backend no PC: esqueleto inicial com protocolo e servidor TCP para testes
- Bluetooth no PC: placeholder (a implementar)
- PSVita: placeholder

## Como testar o backend (sem PSVita)
1) Entrar em `pc-backend/`
2) Executar: `python -m bluetoothmyvita --transport tcp`