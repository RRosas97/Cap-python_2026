import asyncio
import time

import httpx

URLS = ["https://httpbin.org/delay/1" for _ in range(10)]
MAX_CONCURRENTES = 5


async def fetch_una(
    cliente: httpx.AsyncClient, url: str, semaforo: asyncio.Semaphore
) -> int:
    async with semaforo:
        respuesta = await cliente.get(url, timeout=10)
        return respuesta.status_code


async def fetch_todas(urls: list[str]) -> list[int]:
    semaforo = asyncio.Semaphore(MAX_CONCURRENTES)

    async with httpx.AsyncClient() as cliente:
        tareas = [fetch_una(cliente, url, semaforo) for url in urls]
        return await asyncio.gather(*tareas)


def main():
    inicio = time.perf_counter()
    resultados = asyncio.run(fetch_todas(URLS))
    duracion = time.perf_counter() - inicio

    print(f"Códigos de estado: {resultados}")
    print(f"Tiempo total (async, max {MAX_CONCURRENTES} concurrentes): {duracion:.2f}s")


if __name__ == "__main__":
    main()
