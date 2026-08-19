# Declaración de función.
def any_function():
    print("Se imprimió algo.")


any_function()


# Función con parámetros por nombre.
def name_key_params_function(x, y):
    print(f" {x}. {y}.")


name_key_params_function(y="Hola", x="Mundo")


# Función con parámetros posicionales
def positional_params_function(x, y):
    print(f"{x} {y}")


positional_params_function("Hola", "Mundo")


# Función con argumentos variables
def variable_arguments_function(*args):
    return sum(args)


suma1 = variable_arguments_function(2, 5)  # 7
suma2 = variable_arguments_function(5, 8, 9, 4, 20)  # 46
print(f"{suma1}, {suma2}")


# función con argumentos variables (diccionario).
def variable_arguments_dictionary_function(**kwargs):
    for key, value in kwargs.items():
        print(key, "=", value)


variable_arguments_dictionary_function(a=3, b=10, c=3)
variable_arguments_dictionary_function(a="Hola", b="Cómo", c="Estás")

# Función lambda
personas = [{"nombre": "Ana", "edad": 30}, {"nombre": "Luis", "edad": 25}]

personas_ordenadas = sorted(personas, key=lambda p: p["edad"])


# Closures
def crear_saludo(nombre):
    def saludar():
        print(f"Hola, {nombre}")

    return saludar


saludo_ana = crear_saludo("Ana")
saludo_luis = crear_saludo("Luis")

saludo_ana()  # Hola, Ana
saludo_luis()  # Hola, Luis


# Decoradores
def decorador(func):
    def wrapper():
        print("Antes de ejecutar la función")
        func()
        print("Después de ejecutar la función")

    return wrapper


@decorador
def saludar():
    print("Hola!")


saludar()  # Antes de ejecutar la función
# Hola!
# Después de ejecutar la función

# Iteradores
lista = [5, 4, 9, 2]
for elemento in lista:
    print(elemento)


# Generadores
def generador():
    n = 1
    yield n

    n += 1
    yield n

    n += 1
    yield n


for i in generador():
    print(i)
# Salida: 1, 2, 3

# Comprensión de listas
numeros = [1, 2, 3, 4, 5]
cuadrados = [n**2 for n in numeros]
# [1, 4, 9, 16, 25]
# Comprensión de listas con condicional
etiquetas = ["par" if n % 2 == 0 else "impar" for n in numeros]
# ['impar', 'par', 'impar', 'par', 'impar']

# Comprensión de diccionarios
personas = ["Ana", "Luis", "Marco"]
longitudes = {nombre: len(nombre) for nombre in personas}
# {'Ana': 3, 'Luis': 4, 'Marco': 5}

# Comprensión de sets
edades_unicas = {p["edad"] for p in personas}
# {17, 30} -> sin duplicados, porque es un set

# Gestores de contexto(with)
with open("fichero.txt", "w") as fichero:
    fichero.write("Hola!")
