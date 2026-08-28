from dataclasses import dataclass
from typing import Protocol

# =========================
# ENTIDADES DEL DOMINIO
# =========================

@dataclass
class Producto:
    id: int
    nombre: str
    stock: int


@dataclass
class Orden:
    id: int
    producto_id: int
    cantidad: int


# =========================
# REPOSITORIOS
# =========================

class ProductoRepository(Protocol):
    def obtener_por_id(self, producto_id: int) -> Producto | None:
        ...

    def guardar(self, producto: Producto) -> None:
        ...


class OrdenRepository(Protocol):
    def guardar(self, orden: Orden) -> None:
        ...


class ProductoRepositoryMemoria:
    def __init__(self, productos: dict[int, Producto]):
        # Simula la tabla de productos.
        self.productos = productos

    def obtener_por_id(self, producto_id: int) -> Producto | None:
        return self.productos.get(producto_id)

    def guardar(self, producto: Producto) -> None:
        # En memoria el objeto ya fue modificado, pero el método existe
        # para representar que en una DB aquí haríamos un UPDATE.
        self.productos[producto.id] = producto


class OrdenRepositoryMemoria:
    def __init__(self, ordenes: list[Orden]):
        # Simula la tabla de órdenes.
        self.ordenes = ordenes

    def guardar(self, orden: Orden) -> None:
        # En una DB aquí sería algo similar a INSERT INTO ordenes ...
        self.ordenes.append(orden)


# =========================
# UNIDAD DE TRABAJO
# =========================

class UnidadDeTrabajo(Protocol):
    """
    El caso de uso no conoce una transacción concreta de SQL Server,
    SQLAlchemy u otro motor. Solo conoce este contrato.
    """

    productos: ProductoRepository
    ordenes: OrdenRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class UnidadDeTrabajoMemoria:
    """
    Simula una transacción.

    Para hacerlo simple, toma una copia del estado inicial.
    Si ocurre un error y se llama rollback(), restaura esa copia.
    """

    def __init__(
        self,
        productos: dict[int, Producto],
        ordenes: list[Orden],
    ):
        self._productos_originales = {
            producto_id: Producto(
                id=producto.id,
                nombre=producto.nombre,
                stock=producto.stock,
            )
            for producto_id, producto in productos.items()
        }

        self._ordenes_originales = list(ordenes)

        # Los repositorios trabajan sobre los datos actuales.
        self.productos = ProductoRepositoryMemoria(productos)
        self.ordenes = OrdenRepositoryMemoria(ordenes)

        self.confirmado = False

    def commit(self) -> None:
        # En una base de datos real aquí sería connection.commit().
        self.confirmado = True
        print("Cambios confirmados.")

    def rollback(self) -> None:
        # Restauramos los datos al estado que tenían antes de iniciar.
        self.productos.productos.clear()
        self.productos.productos.update(self._productos_originales)

        self.ordenes.ordenes.clear()
        self.ordenes.ordenes.extend(self._ordenes_originales)

        print("Cambios revertidos.")


# =========================
# CASO DE USO
# =========================

class CrearOrden:
    def __init__(self, uow: UnidadDeTrabajo):
        # Recibe una Unidad de Trabajo, no repositorios por separado.
        # Así controla todos los cambios de una sola transacción.
        self.uow = uow

    def ejecutar(
        self,
        orden_id: int,
        producto_id: int,
        cantidad: int,
    ) -> Orden:
        try:
            producto = self.uow.productos.obtener_por_id(producto_id)

            if producto is None:
                raise ValueError("El producto no existe")

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")

            if producto.stock < cantidad:
                raise ValueError("No hay suficiente inventario")

            # Cambio 1: descontar inventario.
            producto.stock -= cantidad
            self.uow.productos.guardar(producto)

            # Cambio 2: guardar la orden.
            orden = Orden(
                id=orden_id,
                producto_id=producto_id,
                cantidad=cantidad,
            )
            self.uow.ordenes.guardar(orden)

            # Si todo salió bien, se confirman todos los cambios.
            self.uow.commit()

            return orden

        except Exception:
            # Si falla cualquiera de los pasos, se deshacen todos.
            self.uow.rollback()
            raise


# =========================
# USO DEL EJEMPLO
# =========================

productos = {
    1: Producto(id=1, nombre="Teclado", stock=5),
}
ordenes: list[Orden] = []

uow = UnidadDeTrabajoMemoria(productos, ordenes)
caso_uso = CrearOrden(uow)

# Caso correcto: se descuenta stock y se registra la orden.
orden = caso_uso.ejecutar(
    orden_id=100,
    producto_id=1,
    cantidad=2,
)

print(orden)
print(productos[1])  # stock = 3
print(ordenes)       # contiene la orden creada