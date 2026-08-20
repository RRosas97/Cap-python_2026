import time
from multiprocessing import Process, cpu_count


def contador(num: int):
    cont = 0
    while cont < num:
        cont += 1


def main():
    inicio = time.perf_counter()
    # a = Process(target=contador, args=(1000000000,)) 35 segundos con un sólo proceso
    a = Process(target=contador, args=(250000000,))
    b = Process(target=contador, args=(250000000,))
    c = Process(target=contador, args=(250000000,))
    d = Process(target=contador, args=(250000000,))
    a.start()
    b.start()
    c.start()
    d.start()

    a.join()
    b.join()
    c.join()
    d.join()
    fin = time.perf_counter()
    total = fin - inicio
    print(f"{total} segundos")
    print(cpu_count())


if __name__ == "__main__":
    main()
