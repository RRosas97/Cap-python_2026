from pathlib import Path

import httpx
from httpx_retries import Retry, RetryTransport


def descargar_archivo(url, destino):
    retry = Retry(total=5, backoff_factor=0.5)
    transport = RetryTransport(retry=retry)
    with httpx.Client(timeout=10.0, transport=transport) as cliente:
        with cliente.stream("GET", url) as respuesta:
            respuesta.raise_for_status()

            destino.parent.mkdir(parents=True, exist_ok=True)

            with open(destino, "wb") as archivo:
                for chunk in respuesta.iter_bytes():
                    archivo.write(chunk)
    print(f"Descarga completa: {destino}")


if __name__ == "__main__":
    url = "https://static.wikia.nocookie.net/videojuego/images/1/17/Crash_Bandicoot_%28Dise%C3%B1o_Actual%29.png/revision/latest?cb=20250214023528"
    destino = Path("descargas") / "crash.png"

    descargar_archivo(url, destino)
