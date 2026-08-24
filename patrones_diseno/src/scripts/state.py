from abc import ABC, abstractmethod


class EstadoOrden(ABC):
    @abstractmethod
    def pagar(self, orden: "Orden") -> None: ...

    @abstractmethod
    def enviar(self, orden: "Orden") -> None: ...

    @abstractmethod
    def cancelar(self, orden: "Orden") -> None: ...


class Pendiente(EstadoOrden):
    def pagar(self, orden: "Orden") -> None:
        print("  Pago recibido -> pasa a Pagado")
        orden.estado = Pagado()

    def enviar(self, orden: "Orden") -> None:
        print("  ERROR: no se puede enviar una orden que no se ha pagado")

    def cancelar(self, orden: "Orden") -> None:
        print("  Orden cancelada")
        orden.estado = Cancelada()


class Pagado(EstadoOrden):
    def pagar(self, orden: "Orden") -> None:
        print("  ERROR: esta orden ya fue pagada")

    def enviar(self, orden: "Orden") -> None:
        print("  Orden enviada -> pasa a Enviado")
        orden.estado = Enviada()

    def cancelar(self, orden: "Orden") -> None:
        print("  Orden pagada cancelada, se procesa reembolso")
        orden.estado = Cancelada()


class Enviada(EstadoOrden):
    def pagar(self, orden: "Orden") -> None:
        print("  ERROR: esta orden ya fue pagada y enviada")

    def enviar(self, orden: "Orden") -> None:
        print("  ERROR: esta orden ya fue enviada")

    def cancelar(self, orden: "Orden") -> None:
        print("  ERROR: no se puede cancelar una orden ya enviada")


class Cancelada(EstadoOrden):
    def pagar(self, orden: "Orden") -> None:
        print("  ERROR: no se puede pagar una orden cancelada")

    def enviar(self, orden: "Orden") -> None:
        print("  ERROR: no se puede enviar una orden cancelada")

    def cancelar(self, orden: "Orden") -> None:
        print("  ERROR: esta orden ya está cancelada")


class Orden:
    def __init__(self):
        self.estado: EstadoOrden = Pendiente()

    def pagar(self) -> None:
        self.estado.pagar(self)

    def enviar(self) -> None:
        self.estado.enviar(self)

    def cancelar(self) -> None:
        self.estado.cancelar(self)


if __name__ == "__main__":
    orden = Orden()

    orden.enviar()  # error: aún pendiente
    orden.pagar()  # ok -> pasa a Pagado
    orden.pagar()  # error: ya pagada
    orden.enviar()  # ok -> pasa a Enviada
    orden.cancelar()  # error: ya no se puede cancelar
