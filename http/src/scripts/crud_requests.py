import requests

# GET
respuesta = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1},
)
print(respuesta.url)  # https://jsonplaceholder.typicode.com/posts?userId=1

# POST
nuevo_post = {
    "title": "Mi primer post",
    "body": "Contenido del post",
    "userId": 1,
}

respuesta = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=nuevo_post,
)

print(respuesta.status_code)
print(respuesta.json())

# PUT
post_actualizado = {
    "id": 1,
    "title": "Título actualizado",
    "body": "Contenido actualizado",
    "userId": 1,
}

respuesta = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json=post_actualizado,
)

print(respuesta.status_code)  # 200
print(respuesta.json())

# PATCH
respuesta = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "Solo cambio el título"},
)


# DELETE
respuesta = requests.delete("https://jsonplaceholder.typicode.com/posts/1")

print(respuesta.status_code)

# MANEJO DE ERRORES
try:
    respuesta = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    respuesta.raise_for_status()  # lanza una excepción si el status code indica error
    print(respuesta.json())
except requests.exceptions.HTTPError as error:
    print(f"Error HTTP: {error}")
except requests.exceptions.ConnectionError:
    print("No se pudo conectar — revisa tu internet o la URL")
except requests.exceptions.Timeout:
    print("La petición tardó demasiado")

# TIMEOUT
respuesta = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1",
    timeout=10,  # segundos
)
