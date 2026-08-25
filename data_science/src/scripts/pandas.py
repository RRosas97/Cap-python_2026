import pandas as pd

# 1. pd.DataFrame() -> crear un DataFrame desde un diccionario
df = pd.DataFrame(
    {
        "producto": ["Café", "Té", "Croissant", "Pan", "Muffin"],
        "categoria": ["Bebidas", "Bebidas", "Panadería", "Panadería", "Panadería"],
        "precio": [45.0, 30.0, 28.5, 35.0, 32.0],
        "cantidad": [3, 5, 4, 6, 3],
    }
)
print("1. DataFrame creado:")
print(df)

# 2. pd.Series() -> una sola columna/lista con índice
serie = pd.Series([1, 2, 3], name="numeros")
print("\n2. Series:")
print(serie)

# 3. pd.read_csv() / df.to_csv() -> leer y escribir CSV
df.to_csv("ventas.csv", index=False)
df_leido = pd.read_csv("ventas.csv")
print("\n3. Leído desde CSV:")
print(df_leido.head(2))

# 4. df.head() / df.tail() -> primeras / últimas filas
print("\n4. head(2):")
print(df.head(2))

# 5. df.info() -> resumen de tipos de datos y valores nulos
print("\n5. info():")
df.info()

# 6. df.describe() -> estadísticas descriptivas rápidas
print("\n6. describe():")
print(df.describe())

# 7. df.shape -> dimensiones (filas, columnas)
print("\n7. shape:", df.shape)

# 8. df.columns / df.dtypes -> nombres y tipos de columnas
print("\n8. columns:", list(df.columns))
print("   dtypes:\n", df.dtypes)

# 9. df['columna'] / df.columna -> seleccionar una columna (regresa una Series)
print("\n9. df['precio']:")
print(df["precio"])

# 10. df[['col1', 'col2']] -> seleccionar varias columnas (regresa un DataFrame)
print("\n10. df[['producto', 'precio']]:")
print(df[["producto", "precio"]])

# 11. df.loc[] -> seleccionar por ETIQUETA (nombre de fila/columna)
print("\n11. loc[0, 'producto']:", df.loc[0, "producto"])
print("    loc[0:2, ['producto', 'precio']]:")
print(df.loc[0:2, ["producto", "precio"]])

# 12. df.iloc[] -> seleccionar por POSICIÓN numérica (como listas normales)
print("\n12. iloc[0]:")
print(df.iloc[0])
print("    iloc[0:2, 0:2]:")
print(df.iloc[0:2, 0:2])

# 13. Filtrado booleano -> df[condición]
print("\n13. df[df['precio'] > 30]:")
print(df[df["precio"] > 30])

# 14. df.query() -> filtrar con una expresión en texto (alternativa legible)
print("\n14. query('precio > 30 and cantidad < 5'):")
print(df.query("precio > 30 and cantidad < 5"))

# 15. df.sort_values() -> ordenar filas por una o más columnas
print("\n15. sort_values('precio', ascending=False):")
print(df.sort_values("precio", ascending=False))

# 16. df['nueva'] = ... -> crear/modificar una columna
df["total"] = df["precio"] * df["cantidad"]
print("\n16. columna 'total' agregada:")
print(df)

# 17. df.apply() -> aplicar una función a cada fila o columna
df["precio_con_iva"] = df["precio"].apply(lambda x: round(x * 1.16, 2))
print("\n17. apply() para calcular precio con IVA:")
print(df[["producto", "precio", "precio_con_iva"]])

# 18. df.map() -> transformar cada valor de una Series (mapeo simple)
traducciones = {"Bebidas": "Beverages", "Panadería": "Bakery"}
print("\n18. map() para traducir categorías:")
print(df["categoria"].map(traducciones))

# 19. df.groupby() -> agrupar filas (equivalente a GROUP BY en SQL)
print("\n19. groupby('categoria')['precio'].mean():")
print(df.groupby("categoria")["precio"].mean())

# 20. df.groupby().agg() -> varias agregaciones a la vez
print("\n20. groupby().agg() con varias métricas:")
print(
    df.groupby("categoria").agg(
        precio_promedio=("precio", "mean"),
        cantidad_total=("cantidad", "sum"),
    )
)

# 21. df.merge() -> unir dos DataFrames (equivalente a JOIN en SQL)
categorias_info = pd.DataFrame(
    {
        "categoria": ["Bebidas", "Panadería"],
        "impuesto": [0.16, 0.08],
    }
)
print("\n21. merge():")
print(df.merge(categorias_info, on="categoria", how="left"))

# 22. df.concat() -> apilar/unir DataFrames verticalmente u horizontalmente
otro_df = pd.DataFrame(
    {
        "producto": ["Bagel"],
        "categoria": ["Panadería"],
        "precio": [27.0],
        "cantidad": [2],
        "total": [54.0],
        "precio_con_iva": [31.32],
    }
)
print("\n22. pd.concat([df, otro_df]):")
print(pd.concat([df, otro_df], ignore_index=True).tail(3))

# 23. df.drop_duplicates() -> eliminar filas duplicadas
print("\n23. drop_duplicates('categoria'):")
print(df.drop_duplicates(subset="categoria"))

# 24. df.dropna() -> eliminar filas con valores nulos
con_nulos = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
print("\n24. dropna():")
print(con_nulos.dropna())

# 25. df.fillna() -> rellenar valores nulos
print("\n25. fillna(0):")
print(con_nulos.fillna(0))

# 26. df.isnull() / df.isna() -> detectar valores nulos
print("\n26. isnull():")
print(con_nulos.isnull())

# 27. df.rename() -> renombrar columnas
print("\n27. rename({'precio': 'precio_unitario'}):")
print(df.rename(columns={"precio": "precio_unitario"}).head(2))

# 28. df.drop() -> eliminar columnas o filas
print("\n28. drop(columns=['precio_con_iva']):")
print(df.drop(columns=["precio_con_iva"]).head(2))

# 29. df.astype() -> convertir el tipo de dato de una columna
print("\n29. astype(int) sobre cantidad:")
print(df["cantidad"].astype(float).head(2))

# 30. df.value_counts() -> contar ocurrencias de cada valor
print("\n30. value_counts('categoria'):")
print(df["categoria"].value_counts())

# 31. df.pivot_table() -> tabla dinámica con agregación integrada
ventas_dias = pd.DataFrame(
    {
        "categoria": ["Bebidas", "Bebidas", "Panadería", "Panadería"],
        "dia": ["Lunes", "Martes", "Lunes", "Martes"],
        "total": [100, 150, 80, 90],
    }
)
print("\n31. pivot_table():")
print(ventas_dias.pivot_table(values="total", index="categoria", columns="dia"))

# 32. df.melt() -> lo inverso a pivot_table (columnas -> filas, formato largo
ancho = ventas_dias.pivot_table(
    values="total", index="categoria", columns="dia"
).reset_index()
print("\n32. melt() de vuelta a formato largo:")
print(ancho.melt(id_vars="categoria", var_name="dia", value_name="total"))

# 33. df.set_index() / df.reset_index() -> cambiar cuál columna es el índice
print("\n33. set_index('producto'):")
print(df.set_index("producto").head(2))

# 34. df.iterrows() -> iterar fila por fila (usar con moderación, es lento)
print("\n34. iterrows() (primeras 2 filas):")
for indice, fila in df.head(2).iterrows():
    print(f"   fila {indice}: {fila['producto']} cuesta ${fila['precio']}")

# 35. df.to_dict() / df.to_numpy() -> convertir a otras estructuras de datos
print("\n35. to_dict('records') (lista de diccionarios, útil para JSON):")
print(df[["producto", "precio"]].head(2).to_dict(orient="records"))
