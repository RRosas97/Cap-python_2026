import timeit
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count


def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def contar_primos(rango: tuple[int, int]) -> int:
    inicio, fin = rango
    return sum(1 for n in range(inicio, fin) if es_primo(n))


RANGOS = [
    (1, 250_000),
    (250_000, 500_000),
    (500_000, 750_000),
    (750_000, 1_000_000),
]


def version_secuencial() -> int:
    return sum(contar_primos(r) for r in RANGOS)


def version_paralela() -> int:
    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        resultados = pool.map(contar_primos, RANGOS)
        return sum(resultados)


if __name__ == "__main__":
    tiempo_secuencial = timeit.timeit(version_secuencial, number=1)
    print(f"Secuencial: {tiempo_secuencial:.2f}s")

    tiempo_paralelo = timeit.timeit(version_paralela, number=1)
    print(f"Con ProcessPoolExecutor ({cpu_count()} núcleos): {tiempo_paralelo:.2f}s")

    print(f"Speedup: {tiempo_secuencial / tiempo_paralelo:.2f}x")
