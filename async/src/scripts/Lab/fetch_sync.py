import time

import httpx

URLS = ["https://httpbin.org/delay/1" for _ in range(10)]


def fetch_todas_sync(urls: list[str]) -> list[int]:
    resultados = []
    with httpx.Client() as cliente:
        for url in urls:
            respuesta = cliente.get(url, timeout=10)
            resultados.append(respuesta.status_code)
    return resultados


def main():
    inicio = time.perf_counter()
    resultados = fetch_todas_sync(URLS)
    duracion = time.perf_counter() - inicio

    print(f"Códigos de estado: {resultados}")
    print(f"Tiempo total (síncrono, una por una): {duracion:.2f}s")


if __name__ == "__main__":
    main()
