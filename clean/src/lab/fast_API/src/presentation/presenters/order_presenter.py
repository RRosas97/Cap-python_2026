from lab.fast_API.src.application.dtos import OrderDTO
from lab.fast_API.src.presentation.schemas import OrderItemOut, OrderOut


class OrderPresenter:
    @staticmethod
    def present(dto: OrderDTO) -> OrderOut:
        return OrderOut(
            id=dto.id,
            user_id=dto.user_id,
            status=dto.status,
            created_at=dto.created_at,
            items=[
                OrderItemOut(
                    id=i.id, product_name=i.product_name, quantity=i.quantity,
                    unit_price=i.unit_price, subtotal=i.subtotal,
                )
                for i in dto.items
            ],
            total=dto.total,
        )

    @staticmethod
    def present_list(dtos: list[OrderDTO]) -> list[OrderOut]:
        return [OrderPresenter.present(d) for d in dtos]
