from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def actualizar(self, orden_id: int, nuevo_estado: str) -> None: ...


class NotificadorEmail(Observador):
    def actualizar(self, orden_id: int, nuevo_estado: str) -> None:
        print
        (f"  [Email] Orden {orden_id} cambió a '{nuevo_estado}' -- mandando correo")


class NotificadorSMS(Observador):
    def actualizar(self, orden_id: int, nuevo_estado: str) -> None:
        print(f"  [SMS] Orden {orden_id} cambió a '{nuevo_estado}' -- mandando SMS")


class RegistroAuditoria(Observador):
    def actualizar(self, orden_id: int, nuevo_estado: str) -> None:
        print(f"  [Auditoría] Log: orden {orden_id} -> {nuevo_estado}")


class OrdenObservable:

    def __init__(self, orden_id: int):
        self.orden_id = orden_id
        self.estado = "pendiente"
        self._observadores: list[Observador] = []

    def suscribir(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def cambiar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado
        for observador in self._observadores:
            observador.actualizar(self.orden_id, nuevo_estado)


if __name__ == "__main__":
    orden = OrdenObservable(orden_id=42)
    orden.suscribir(NotificadorEmail())
    orden.suscribir(NotificadorSMS())
    orden.suscribir(RegistroAuditoria())

    orden.cambiar_estado("pagado")
    print()
    orden.cambiar_estado("enviado")
