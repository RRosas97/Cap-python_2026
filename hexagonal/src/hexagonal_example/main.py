from application.dtos import CrearUsuarioDTO
from application.use_cases import (
    CrearUsuarioUseCase,
    EliminarUsuarioUseCase,
    ListarUsuariosUseCase,
)
from infrastructure.memory_repository import InMemoryUserRepository


def main():
    # Aquí, y SOLO aquí, se conecta la infraestructura concreta
    # con los casos de uso -- este es el único lugar que "sabe"
    # que estamos usando memoria y no SQL.
    repositorio = InMemoryUserRepository()

    crear_usuario = CrearUsuarioUseCase(repositorio)
    eliminar_usuario = EliminarUsuarioUseCase(repositorio)
    listar_usuarios = ListarUsuariosUseCase(repositorio)

    print("=== Creando usuarios ===")
    ana = crear_usuario.ejecutar(CrearUsuarioDTO(nombre="Ana", email="ana@mail.com"))
    luis = crear_usuario.ejecutar(CrearUsuarioDTO(nombre="Luis", email="luis@mail.com"))
    print(f"Creado: {ana}")
    print(f"Creado: {luis}")

    print("\n=== Listando usuarios ===")
    for usuario in listar_usuarios.ejecutar():
        print(f" - {usuario}")

    print(f"\n=== Eliminando a {ana.nombre} (id={ana.id}) ===")
    eliminado = eliminar_usuario.ejecutar(ana.id)
    print(f"¿Se eliminó?: {eliminado}")

    print("\n=== Listando de nuevo (Ana ya no debería aparecer) ===")
    for usuario in listar_usuarios.ejecutar():
        print(f" - {usuario}")

    print("\n=== Probando validación de la entidad (nombre vacío) ===")
    try:
        crear_usuario.ejecutar(CrearUsuarioDTO(nombre="", email="x@mail.com"))
    except ValueError as error:
        print(f"Error esperado: {error}")


if __name__ == "__main__":
    main()
