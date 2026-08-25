import polars as pl

# 1. pl.DataFrame() -> crear un DataFrame desde un diccionario
df = pl.DataFrame(
    {
        "producto": ["Café", "Té", "Croissant", "Pan", "Muffin"],
        "categoria": ["Bebidas", "Bebidas", "Panadería", "Panadería", "Panadería"],
        "precio": [45.0, 30.0, 28.5, 35.0, 32.0],
        "cantidad": [3, 5, 4, 6, 3],
    }
)
print("1. DataFrame creado:")
print(df)


# 2. pl.read_csv() / df.write_csv() -> leer y escribir CSV
df.write_csv("ventas.csv")
df_leido = pl.read_csv("ventas.csv")
print("\n2. Leído desde CSV:")
print(df_leido.head(2))


# 3. df.head() / df.tail() -> primeras / últimas filas
print("\n3. head(2):")
print(df.head(2))
print("tail(2):")
print(df.tail(2))


# 4. df.select() -> elegir columnas específicas
print("\n4. select(producto, precio):")
print(df.select("producto", "precio"))


# 5. df.filter() -> filtrar filas (equivalente a WHERE en SQL)
print("\n5. filter(precio > 30):")
print(df.filter(pl.col("precio") > 30))


# 6. df.with_columns() -> agregar o modificar columnas
print("\n6. with_columns(total = precio * cantidad):")
df_con_total = df.with_columns((pl.col("precio") * pl.col("cantidad")).alias("total"))
print(df_con_total)


# 7. df.sort() -> ordenar filas
print("\n7. sort('precio', descending=True):")
print(df.sort("precio", descending=True))


# 8. df.group_by().agg() -> agrupar y agregar (equivalente a GROUP BY)
print("\n8. group_by('categoria').agg(suma y promedio):")
print(
    df.group_by("categoria").agg(
        pl.col("precio").mean().alias("precio_promedio"),
        pl.col("cantidad").sum().alias("cantidad_total"),
    )
)


# 9. df.join() -> unir dos DataFrames (equivalente a JOIN en SQL)
categorias_info = pl.DataFrame(
    {
        "categoria": ["Bebidas", "Panadería"],
        "impuesto": [0.16, 0.08],
    }
)
print("\n9. join con otra tabla:")
print(df.join(categorias_info, on="categoria", how="left"))


# 10. df.unique() -> eliminar duplicados
print("\n10. unique('categoria'):")
print(df.select("categoria").unique())


# 11. df.drop_nulls() -> eliminar filas con valores nulos
df_con_nulos = pl.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
print("\n11. drop_nulls():")
print(df_con_nulos.drop_nulls())


# 12. df.fill_null() -> rellenar valores nulos
print("\n12. fill_null(0):")
print(df_con_nulos.fill_null(0))


# 13. df.describe() -> estadísticas descriptivas rápidas
print("\n13. describe():")
print(df.describe())


# 14. df.rename() -> renombrar columnas
print("\n14. rename({'precio': 'precio_unitario'}):")
print(df.rename({"precio": "precio_unitario"}).head(2))


# 15. df.drop() -> eliminar columnas
print("\n15. drop('categoria'):")
print(df.drop("categoria").head(2))


# 16. pl.when().then().otherwise() -> lógica condicional (como un CASE WHEN de SQL)
print("\n16. when/then/otherwise:")
print(
    df.with_columns(
        pl.when(pl.col("precio") > 30)
        .then(pl.lit("caro"))
        .otherwise(pl.lit("barato"))
        .alias("etiqueta")
    )
)


# 17. df.pivot() -> reorganizar filas en columnas (tabla dinámica)
ventas_por_dia = pl.DataFrame(
    {
        "categoria": ["Bebidas", "Bebidas", "Panadería", "Panadería"],
        "dia": ["Lunes", "Martes", "Lunes", "Martes"],
        "total": [100, 150, 80, 90],
    }
)
print("\n17. pivot(dia como columnas):")
print(ventas_por_dia.pivot(values="total", index="categoria", on="dia"))


# 18. df.unpivot() -> lo inverso a pivot (columnas -> filas, "melt")
pivot_result = ventas_por_dia.pivot(values="total", index="categoria", on="dia")
print("\n18. unpivot() de vuelta a formato largo:")
print(pivot_result.unpivot(index="categoria", variable_name="dia", value_name="total"))


# 19. df.lazy() / .collect() -> evaluación perezosa, para optimizar consultas grandes
print("\n19. lazy() + collect() (equivalente perezoso a lo de arriba):")
resultado_lazy = (
    df.lazy()
    .filter(pl.col("precio") > 25)
    .group_by("categoria")
    .agg(pl.col("cantidad").sum())
    .collect()  # aquí es donde REALMENTE se ejecuta todo, de forma optimizada
)
print(resultado_lazy)


# 20. df.sample() -> tomar una muestra aleatoria de filas
print("\n20. sample(n=2):")
print(df.sample(n=2, seed=42))
