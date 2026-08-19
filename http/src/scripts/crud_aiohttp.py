import asyncio

import aiohttp

# CRUD asíncrono
BASE_URL = "https://jsonplaceholder.typicode.com/posts"


async def crear_post(sesion, titulo, contenido, usuario_id):
    async with sesion.post(
        BASE_URL,
        json={"title": titulo, "body": contenido, "userId": usuario_id},
    ) as respuesta:
        return await respuesta.json()


async def leer_post(sesion, post_id):
    async with sesion.get(f"{BASE_URL}/{post_id}") as respuesta:
        return await respuesta.json()


async def actualizar_post(sesion, post_id, titulo):
    async with sesion.patch(
        f"{BASE_URL}/{post_id}",
        json={"title": titulo},
    ) as respuesta:
        return await respuesta.json()


async def eliminar_post(sesion, post_id):
    async with sesion.delete(f"{BASE_URL}/{post_id}") as respuesta:
        return respuesta.status == 200


async def main():
    async with aiohttp.ClientSession() as sesion:
        nuevo = await crear_post(sesion, "Mi post", "contenido", 1)
        print(nuevo)

        post = await leer_post(sesion, 1)
        print(post)

        actualizado = await actualizar_post(sesion, 1, "Titulo nuevo")
        print(actualizado)

        eliminado = await eliminar_post(sesion, 1)
        print(eliminado)


asyncio.run(main())


# Múltiples peticiones paralelas
async def leer_varios_posts(ids):
    async with aiohttp.ClientSession() as sesion:
        tareas = [leer_post(sesion, id) for id in ids]
        resultados = await asyncio.gather(*tareas)
        return resultados


posts = asyncio.run(leer_varios_posts([1, 2, 3, 4, 5]))
print(posts)


# Manejo de errores
async def leer_post_seguro(sesion, post_id):
    try:
        async with sesion.get(f"{BASE_URL}/{post_id}") as respuesta:
            respuesta.raise_for_status()
            return await respuesta.json()
    except aiohttp.ClientResponseError as error:
        print(f"Error HTTP: {error}")
    except aiohttp.ClientConnectionError:
        print("No se pudo conectar")
