async def registrar_y_loguear(client, username="ana", password="Password123"):
    """Helper: registra un usuario y regresa su token de acceso."""
    await client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@mail.com",
            "password": password,
        },
    )

    respuesta = await client.post(
        "/auth/login",
        data={"username": username, "password": password},  # form-data, no json
    )
    token = respuesta.json()["access_token"]
    return token


# ---------- Registro y login ----------


async def test_registro_exitoso(client):
    respuesta = await client.post(
        "/auth/register",
        json={"username": "ana", "email": "ana@mail.com", "password": "Password123"},
    )

    assert respuesta.status_code == 200
    data = respuesta.json()
    assert data["username"] == "ana"
    assert "password" not in data
    assert "hashed_password" not in data


async def test_registro_username_duplicado(client):
    payload = {"username": "ana", "email": "ana@mail.com", "password": "Password123"}
    await client.post("/auth/register", json=payload)

    respuesta = await client.post("/auth/register", json=payload)

    assert respuesta.status_code == 400


async def test_login_credenciales_incorrectas(client):
    await client.post(
        "/auth/register",
        json={"username": "ana", "email": "ana@mail.com", "password": "Password123"},
    )

    respuesta = await client.post(
        "/auth/login",
        data={"username": "ana", "password": "contraseña_incorrecta"},
    )

    assert respuesta.status_code == 401


# ---------- Órdenes: flujo protegido ----------


async def test_crear_orden_sin_token_es_rechazada(client):
    respuesta = await client.post("/orders/", json={"items": []})
    assert respuesta.status_code == 401


async def test_crear_orden_exitosa(client):
    token = await registrar_y_loguear(client)

    respuesta = await client.post(
        "/orders/",
        json={
            "items": [
                {"product_name": "Café", "quantity": 2, "unit_price": 45.0},
                {"product_name": "Té", "quantity": 1, "unit_price": 30.0},
            ]
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 201
    data = respuesta.json()
    assert len(data["items"]) == 2
    assert data["total"] == (2 * 45.0) + (1 * 30.0)


async def test_crear_orden_con_cantidad_invalida(client):
    token = await registrar_y_loguear(client)

    respuesta = await client.post(
        "/orders/",
        json={"items": [{"product_name": "Café", "quantity": -1, "unit_price": 45.0}]},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 422


async def test_crear_orden_sin_items(client):
    token = await registrar_y_loguear(client)

    respuesta = await client.post(
        "/orders/",
        json={"items": []},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 422


async def test_listar_ordenes_solo_muestra_las_propias(client):
    token_ana = await registrar_y_loguear(client, username="ana")
    token_luis = await registrar_y_loguear(client, username="luis")

    await client.post(
        "/orders/",
        json={"items": [{"product_name": "Café", "quantity": 1, "unit_price": 45.0}]},
        headers={"Authorization": f"Bearer {token_ana}"},
    )
    await client.post(
        "/orders/",
        json={"items": [{"product_name": "Té", "quantity": 1, "unit_price": 30.0}]},
        headers={"Authorization": f"Bearer {token_luis}"},
    )

    respuesta = await client.get(
        "/orders/", headers={"Authorization": f"Bearer {token_ana}"}
    )

    ordenes = respuesta.json()
    assert len(ordenes) == 1
    assert ordenes[0]["items"][0]["product_name"] == "Café"


async def test_no_puede_ver_orden_de_otro_usuario(client):
    token_ana = await registrar_y_loguear(client, username="ana")
    token_luis = await registrar_y_loguear(client, username="luis")

    creada = await client.post(
        "/orders/",
        json={"items": [{"product_name": "Café", "quantity": 1, "unit_price": 45.0}]},
        headers={"Authorization": f"Bearer {token_ana}"},
    )
    order_id = creada.json()["id"]

    respuesta = await client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token_luis}"},
    )

    assert respuesta.status_code == 403


async def test_actualizar_status_de_orden(client):
    token = await registrar_y_loguear(client)

    creada = await client.post(
        "/orders/",
        json={"items": [{"product_name": "Café", "quantity": 1, "unit_price": 45.0}]},
        headers={"Authorization": f"Bearer {token}"},
    )
    order_id = creada.json()["id"]

    respuesta = await client.patch(
        f"/orders/{order_id}/status",
        json={"status": "pagado"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "pagado"


async def test_actualizar_status_invalido(client):
    token = await registrar_y_loguear(client)

    creada = await client.post(
        "/orders/",
        json={"items": [{"product_name": "Café", "quantity": 1, "unit_price": 45.0}]},
        headers={"Authorization": f"Bearer {token}"},
    )
    order_id = creada.json()["id"]

    respuesta = await client.patch(
        f"/orders/{order_id}/status",
        json={"status": "estado_que_no_existe"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert respuesta.status_code == 422
