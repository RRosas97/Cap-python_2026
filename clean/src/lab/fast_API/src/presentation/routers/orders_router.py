from fastapi import APIRouter, Depends, status
from lab.fast_API.src.application.dtos import (
    CreateOrderDTO,
    OrderItemInputDTO,
    UpdateOrderStatusDTO,
)
from lab.fast_API.src.application.use_cases.create_order import CreateOrderUseCase
from lab.fast_API.src.application.use_cases.delete_order import DeleteOrderUseCase
from lab.fast_API.src.application.use_cases.get_order import GetOrderUseCase
from lab.fast_API.src.application.use_cases.list_orders import ListOrdersUseCase
from lab.fast_API.src.application.use_cases.update_order_status import (
    UpdateOrderStatusUseCase,
)
from lab.fast_API.src.presentation.dependencies import (
    get_create_order_use_case,
    get_current_user_id,
    get_delete_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
    get_update_order_status_use_case,
)
from lab.fast_API.src.presentation.presenters.order_presenter import OrderPresenter
from lab.fast_API.src.presentation.schemas import (
    OrderCreateRequest,
    OrderOut,
    OrderStatusUpdateRequest,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def crear_orden(
    request: OrderCreateRequest,
    user_id: int = Depends(get_current_user_id),
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    dto = CreateOrderDTO(
        user_id=user_id,
        items=[OrderItemInputDTO(**item.model_dump()) for item in request.items],
    )
    resultado = use_case.ejecutar(dto)
    return OrderPresenter.present(resultado)


@router.get("/", response_model=list[OrderOut])
def listar_mis_ordenes(
    user_id: int = Depends(get_current_user_id),
    use_case: ListOrdersUseCase = Depends(get_list_orders_use_case),
):
    resultado = use_case.ejecutar(user_id)
    return OrderPresenter.present_list(resultado)


@router.get("/{order_id}", response_model=OrderOut)
def obtener_orden(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    use_case: GetOrderUseCase = Depends(get_get_order_use_case),
):
    resultado = use_case.ejecutar(order_id, requesting_user_id=user_id)
    return OrderPresenter.present(resultado)


@router.patch("/{order_id}/status", response_model=OrderOut)
def actualizar_estado(
    order_id: int,
    request: OrderStatusUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    use_case: UpdateOrderStatusUseCase = Depends(get_update_order_status_use_case),
):
    dto = UpdateOrderStatusDTO(order_id=order_id, status=request.status, 
                               requesting_user_id=user_id)
    resultado = use_case.ejecutar(dto)
    return OrderPresenter.present(resultado)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    use_case: DeleteOrderUseCase = Depends(get_delete_order_use_case),
):
    use_case.ejecutar(order_id, requesting_user_id=user_id)
