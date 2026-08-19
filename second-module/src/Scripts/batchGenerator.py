def batch_generator(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i : i + n]


lista = [1, 2, 3, 4, 5, 6, 7]
for lote in batch_generator(lista, 3):
    print(lote)
