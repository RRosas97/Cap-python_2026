from auth import obtener_usuario_actual
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from services import orders_service
from sqlalchemy.orm import Session
from src.models import User
from src.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


def _verificar_propietario(order, usuario_actual: User):
    """Lanza 403 si la orden no pertenece al usuario autenticado."""
    if order.user_id != usuario_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta orden",
        )


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def crear_orden(
    datos: OrderCreate,
    session: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):
    items = [item.model_dump() for item in datos.items]
    orden = orders_service.create_order_with_items(
        session, user_id=usuario_actual.id, items=items
    )
    return orden


@router.get("/", response_model=list[OrderOut])
def listar_mis_ordenes(
    session: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):
    return orders_service.list_orders_by_user(session, user_id=usuario_actual.id)


@router.get("/{order_id}", response_model=OrderOut)
def obtener_orden(
    order_id: int,
    session: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):
    orden = orders_service.get_order(session, order_id)
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    _verificar_propietario(orden, usuario_actual)
    return orden


@router.patch("/{order_id}/status", response_model=OrderOut)
def actualizar_estado(
    order_id: int,
    datos: OrderStatusUpdate,
    session: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):
    orden = orders_service.get_order(session, order_id)
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    _verificar_propietario(orden, usuario_actual)

    actualizada = orders_service.update_order_status(session, order_id, datos.status)
    return actualizada


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(
    order_id: int,
    session: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):
    orden = get_db.get_order(session, order_id)
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    _verificar_propietario(orden, usuario_actual)

    get_db.delete_order(session, order_id)
