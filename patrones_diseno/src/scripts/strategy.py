from abc import ABC, abstractmethod


class EstrategiaEnvio(ABC):
    @abstractmethod
    def calcular_costo(self, peso_kg: float) -> float: ...


class EnvioEstandar(EstrategiaEnvio):
    def calcular_costo(self, peso_kg: float) -> float:
        return 50 + peso_kg * 10


class EnvioExpress(EstrategiaEnvio):
    def calcular_costo(self, peso_kg: float) -> float:
        return 150 + peso_kg * 20


class EnvioGratis(EstrategiaEnvio):
    def calcular_costo(self, peso_kg: float) -> float:
        return 0


class Pedido:
    def __init__(self, peso_kg: float, estrategia: EstrategiaEnvio):
        self.peso_kg = peso_kg
        self._estrategia = estrategia

    def costo_envio(self) -> float:
        return self._estrategia.calcular_costo(self.peso_kg)

    def cambiar_estrategia(self, nueva: EstrategiaEnvio) -> None:
        self._estrategia = nueva


if __name__ == "__main__":
    pedido = Pedido(peso_kg=3, estrategia=EnvioEstandar())
    print(f"Envío estándar: ${pedido.costo_envio()}")

    pedido.cambiar_estrategia(EnvioExpress())
    print(f"Envío express:  ${pedido.costo_envio()}")

    pedido.cambiar_estrategia(EnvioGratis())
    print(f"Envío gratis:   ${pedido.costo_envio()}")
