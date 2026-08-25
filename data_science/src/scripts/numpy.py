import numpy as np

# 1. np.array() -> crear un array desde una lista de Python
arr = np.array([10, 20, 30, 40, 50])
print("1. array creado:", arr)

# 2. np.zeros() / np.ones() -> arrays inicializados en 0 o 1
print("\n2. zeros(5):", np.zeros(5))
print("   ones((2, 3)):\n", np.ones((2, 3)))

# 3. np.arange() -> como range() de Python, pero regresa un array
print("\n3. arange(0, 10, 2):", np.arange(0, 10, 2))

# 4. np.linspace() -> N valores igualmente espaciados entre dos límites
print("\n4. linspace(0, 1, 5):", np.linspace(0, 1, 5))

# 5. arr.shape -> las dimensiones de un array (filas, columnas, ...)
matriz = np.array([[1, 2, 3], [4, 5, 6]])
print("\n5. shape de la matriz:", matriz.shape)  # (2, 3) -> 2 filas, 3 columnas

# 6. arr.reshape() -> cambiar la forma de un array sin cambiar sus datos
plano = np.arange(6)
print("\n6. reshape(2, 3):\n", plano.reshape(2, 3))

# 7. Indexado y slicing -> acceder a elementos o sub-arrays
print("\n7. arr[1:4]:", arr[1:4])
print("   matriz[0, 2] (fila 0, columna 2):", matriz[0, 2])
print("   matriz[:, 1] (toda la columna 1):", matriz[:, 1])

# 8. Indexado booleano -> filtrar con una condición (masking)
print("\n8. arr[arr > 25]:", arr[arr > 25])

# 9. Operaciones vectorizadas -> se aplican a TODO el array de una vez, sin loops
print("\n9. arr * 2:", arr * 2)
print("   arr + arr:", arr + arr)

# 10. np.sum() / arr.sum() -> suma de todos los elementos
print("\n10. sum():", arr.sum())
print("    sum por columna (axis=0):", matriz.sum(axis=0))
print("    sum por fila (axis=1):", matriz.sum(axis=1))

# 11. np.mean() / np.std() -> promedio y desviación estándar
print("\n11. mean():", arr.mean())
print("    std():", arr.std())

# 12. np.min() / np.max() / np.argmax() -> valores extremos y su posición
print("\n12. min():", arr.min(), " max():", arr.max())
print("    argmax() (índice del máximo):", arr.argmax())

# 13. np.sort() -> ordenar un array
desordenado = np.array([5, 2, 8, 1, 9])
print("\n13. sort():", np.sort(desordenado))

# 14. np.unique() -> valores únicos, sin duplicados
repetidos = np.array([1, 2, 2, 3, 3, 3])
print("\n14. unique():", np.unique(repetidos))

# 15. np.concatenate() -> unir arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("\n15. concatenate([a, b]):", np.concatenate([a, b]))

# 16. np.where() -> condicional vectorizado (como un if/else aplicado a todo el array)
print("\n16. where(arr > 25, 'alto', 'bajo'):", np.where(arr > 25, "alto", "bajo"))

# 17. Broadcasting -> operar arrays de formas distintas sin loops explícitos
matriz_2x3 = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
print("\n17. broadcasting (matriz + vector):\n", matriz_2x3 + vector)

# 18. np.dot() / operador @ -> multiplicación de matrices (producto punto)
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print("\n18. multiplicación de matrices (m1 @ m2):\n", m1 @ m2)

# 19. np.random -> generación de números aleatorios (con semilla para reproducibilidad)
rng = np.random.default_rng(seed=42)
print("\n19. números aleatorios reproducibles:", rng.random(3))

# 20. np.nan / np.isnan() -> manejo de valores faltantes en datos numéricos
con_faltantes = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
print("\n20. isnan():", np.isnan(con_faltantes))
print("    nanmean() (promedio ignorando NaN):", np.nanmean(con_faltantes))
