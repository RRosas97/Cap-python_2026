import pytest
from lab.fast_API.src.application.dtos import CreateOrderDTO, OrderItemInputDTO
from lab.fast_API.src.application.use_cases.create_order import CreateOrderUseCase
from lab.fast_API.src.domain.events import OrderCreated


class FakeOrderRepo:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def add(self, order):
        order.id = self.next_id
        for item in order.items:
            item.id = self.next_id * 100
        self.next_id += 1
        self.data[order.id] = order
        return order

    def get(self, order_id):
        return self.data.get(order_id)

    def list_by_user(self, user_id):
        return [o for o in self.data.values() if o.user_id == user_id]

    def update_status(self, order_id, status):
        o = self.data.get(order_id)
        if o:
            o.status = status
        return o

    def delete(self, order_id):
        return self.data.pop(order_id, None) is not None


class FakeUoW:
    def __init__(self):
        self.orders = FakeOrderRepo()
        self.users = None
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class SpyDispatcher:
    def __init__(self):
        self.eventos_recibidos = []

    def dispatch(self, events):
        self.eventos_recibidos.extend(events)


@pytest.fixture
def uow():
    return FakeUoW()


@pytest.fixture
def dispatcher():
    return SpyDispatcher()


def test_create_order_persiste_la_orden(uow, dispatcher):
    uc = CreateOrderUseCase(uow, dispatcher)

    resultado = uc.ejecutar(
        CreateOrderDTO(
            user_id=1,
            items=[OrderItemInputDTO(product_name="Café", quantity=2, unit_price=45.0)],
        )
    )

    assert resultado.id is not None
    assert uow.orders.get(resultado.id) is not None
    assert uow.committed is True


def test_create_order_despacha_evento_order_created(uow, dispatcher):
    uc = CreateOrderUseCase(uow, dispatcher)

    resultado = uc.ejecutar(
        CreateOrderDTO(
            user_id=1,
            items=[OrderItemInputDTO(product_name="Café", quantity=2, unit_price=45.0)],
        )
    )

    assert len(dispatcher.eventos_recibidos) == 1
    evento = dispatcher.eventos_recibidos[0]
    assert isinstance(evento, OrderCreated)
    assert evento.order_id == resultado.id
    assert evento.user_id == 1
    assert evento.total == 90.0


def test_create_order_sin_items_no_persiste_ni_notifica(uow, dispatcher):
    uc = CreateOrderUseCase(uow, dispatcher)

    with pytest.raises(ValueError):
        uc.ejecutar(CreateOrderDTO(user_id=1, items=[]))

    assert uow.committed is False
    assert dispatcher.eventos_recibidos == []
