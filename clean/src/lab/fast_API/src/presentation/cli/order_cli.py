import typer
from lab.fast_API.src.application.dtos import CreateOrderDTO, OrderItemInputDTO
from lab.fast_API.src.application.errors import ForbiddenError, NotFoundError
from lab.fast_API.src.application.use_cases.create_order import CreateOrderUseCase
from lab.fast_API.src.application.use_cases.delete_order import DeleteOrderUseCase
from lab.fast_API.src.application.use_cases.get_order import GetOrderUseCase
from lab.fast_API.src.application.use_cases.list_orders import ListOrdersUseCase
from lab.fast_API.src.infrastructure.db.session import SessionLocal
from lab.fast_API.src.infrastructure.events.in_memory_dispatcher import (
    InMemoryEventDispatcher,
)
from lab.fast_API.src.infrastructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from rich.console import Console
from rich.table import Table

# Console de rich para imprimir tablas bonitas en la terminal
console = Console()

app = typer.Typer(help="CLI para gestionar órdenes")


def _get_uow():
    session = SessionLocal
    return SQLAlchemyUnitOfWork(session)


def _get_dispatcher():
    return InMemoryEventDispatcher()

@app.command()
def listar(
    user_id: int = typer.Option(..., "--user-id", "-u", help="ID del usuario"),
):
    """
    Lista todas las órdenes de un usuario.
    """
    uow = _get_uow()
    caso_uso = ListOrdersUseCase(uow)

    ordenes = caso_uso.ejecutar(user_id=user_id)

    if not ordenes:
        typer.echo("No se encontraron órdenes.")
        raise typer.Exit()

    tabla = Table(title=f"Órdenes del usuario {user_id}")
    tabla.add_column("ID",       style="cyan")
    tabla.add_column("Status",   style="magenta")
    tabla.add_column("Total",    style="green")
    tabla.add_column("Creada en")

    for orden in ordenes:
        tabla.add_row(
            str(orden.id),
            orden.status,
            f"${orden.total:.2f}",
            str(orden.created_at),
        )

    console.print(tabla)

@app.command()
def obtener(
    order_id: int = typer.Option(..., "--order-id", "-o", help="ID de la orden"),
    user_id:  int = typer.Option(..., "--user-id",  "-u", help="ID del usuario"),
):
    uow = _get_uow()
    caso_uso = GetOrderUseCase(uow)

    try:
        orden = caso_uso.ejecutar(
            order_id=order_id,
            requesting_user_id=user_id,
        )

        console.print(f"\n[bold cyan]Orden #{orden.id}[/bold cyan]")
        console.print(f"Status:  {orden.status}")
        console.print(f"Total:   ${orden.total:.2f}")
        console.print(f"Creada:  {orden.created_at}\n")

        tabla = Table(title="Items")
        tabla.add_column("Producto")
        tabla.add_column("Cantidad")
        tabla.add_column("Precio unitario")
        tabla.add_column("Subtotal")

        for item in orden.items:
            tabla.add_row(
                item.product_name,
                str(item.quantity),
                f"${item.unit_price:.2f}",
                f"${item.subtotal:.2f}",
            )

        console.print(tabla)

    except NotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    except ForbiddenError as e:
        typer.echo(f"Acceso denegado: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def crear(
    user_id:      int   = typer.Option(..., "--user-id",      
                                       "-u", help="ID del usuario"),
    product_name: str   = typer.Option(..., "--product",      
                                       "-p", help="Nombre del producto"),
    quantity:     int   = typer.Option(..., "--quantity",     
                                       "-q", help="Cantidad"),
    unit_price:   float = typer.Option(..., "--unit-price",   
                                       "-r", help="Precio unitario"),
):
    """
    Crea una nueva orden con un item.
    """
    uow        = _get_uow()
    dispatcher = _get_dispatcher()
    caso_uso   = CreateOrderUseCase(uow, dispatcher)
    datos = CreateOrderDTO(
        user_id=user_id,
        items=[
            OrderItemInputDTO(
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
            )
        ],
    )

    orden = caso_uso.ejecutar(datos)

    typer.echo(f"✅ Orden #{orden.id} creada exitosamente. Total: ${orden.total:.2f}")

@app.command()
def eliminar(
    order_id: int = typer.Option(..., "--order-id", "-o", help="ID de la orden"),
    user_id:  int = typer.Option(..., "--user-id",  "-u", help="ID del usuario"),
):

    confirmar = typer.confirm(
        f"¿Estás seguro de eliminar la orden #{order_id}?"
    )

    if not confirmar:
        typer.echo("Operación cancelada.")
        raise typer.Exit()

    uow      = _get_uow()
    caso_uso = DeleteOrderUseCase(uow)

    try:
        caso_uso.ejecutar(
            order_id=order_id,
            requesting_user_id=user_id,
        )
        typer.echo(f"🗑️  Orden #{order_id} eliminada correctamente.")

    except NotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    except ForbiddenError as e:
        typer.echo(f"Acceso denegado: {e}", err=True)
        raise typer.Exit(code=1)