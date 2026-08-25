import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Cargar el CSV
df = pd.read_csv("clientes.csv")
print("Datos crudos:")
print(df)
print(f"\nFilas con valores nulos:\n{df.isnull().sum()}")


# Limpiar los datos
df["edad"] = df["edad"].fillna(df["edad"].median())
df["ingreso_mensual"] = df["ingreso_mensual"].fillna(df["ingreso_mensual"].median())

print("\nDespués de limpiar (fillna con mediana):")
print(df)
print(f"\nFilas con valores nulos ahora: {df.isnull().sum().sum()}")


# Preparar X (features/entradas) e y (target/lo que queremos predecir)

X = df[["edad", "ingreso_mensual", "visitas_web"]]
y = df["compro"]

print(f"\nX (features):\n{X.head()}")
print(f"\ny (target):\n{y.head()}")


#  Dividir en datos de entrenamiento y de prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nDatos de entrenamiento: {len(X_train)} filas")
print(f"Datos de prueba:        {len(X_test)} filas")


# Entrenar el clasificador

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)
print("\nModelo entrenado.")


# Evaluar qué tan bien predice

predicciones_test = modelo.predict(X_test)
precision = accuracy_score(y_test, predicciones_test)
print(f"\nPrecisión en datos de prueba: {precision:.2%}")
print("\nReporte de clasificación:")
print(classification_report(y_test, predicciones_test))


# SERIALIZACIÓN: guardar el modelo entrenado a disco

joblib.dump(modelo, "modelo_clientes.joblib")
print("\nModelo guardado en 'modelo_clientes.joblib'")


# INFERENCIA: cargar el modelo guardado y usarlo con datos NUEVOS
modelo_cargado = joblib.load("modelo_clientes.joblib")
print("Modelo cargado desde disco.")

# Datos de un cliente NUEVO, que el modelo nunca vio antes
cliente_nuevo = pd.DataFrame(
    {
        "edad": [42],
        "ingreso_mensual": [21000],
        "visitas_web": [12],
    }
)

prediccion = modelo_cargado.predict(cliente_nuevo)
probabilidad = modelo_cargado.predict_proba(cliente_nuevo)

print(f"\nCliente nuevo: {cliente_nuevo.to_dict(orient='records')[0]}")
print(f"¿Compra?: {prediccion[0]}")
print(f"Probabilidades [no, si]: {probabilidad[0]}")


# Otro cliente, para confirmar que el modelo distingue casos
cliente_bajo_perfil = pd.DataFrame(
    {
        "edad": [21],
        "ingreso_mensual": [6500],
        "visitas_web": [2],
    }
)

prediccion2 = modelo_cargado.predict(cliente_bajo_perfil)
print(f"\nCliente bajo perfil: {cliente_bajo_perfil.to_dict(orient='records')[0]}")
print(f"¿Compra?: {prediccion2[0]}")
