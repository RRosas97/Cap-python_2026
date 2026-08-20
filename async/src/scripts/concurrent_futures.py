import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

# thread pool executor
# def desayunar():
#     print('Iniciando desayuno...')
#     time.sleep(3)
#     print('Terminando desayuno...')


# def tomar_cafe():
#     print('Iniciando cafe...')
#     time.sleep(4)
#     print('Terminando cafe...')


# def estudiar():
#     print('Iniciando estudiar...')
#     time.sleep(5)
#     print('Terminando estudiar...')


# inicio = time.perf_counter()

# with ThreadPoolExecutor(max_workers=3) as pool:
#     pool.submit(desayunar)
#     pool.submit(tomar_cafe)
#     pool.submit(estudiar)

# fin = time.perf_counter()
# print(f"Tiempo total: {fin - inicio:.2f} segundos")

# PROCESS POOL EXECUTOR


def contador(num: int):
    cont = 0
    while cont < num:
        cont += 1


def main():
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        pool.submit(contador, 250000000)
        pool.submit(contador, 250000000)
        pool.submit(contador, 250000000)
        pool.submit(contador, 250000000)
    fin = time.perf_counter()
    total = fin - inicio
    print(f"{total} segundos")
    print(cpu_count())


if __name__ == "__main__":
    main()
