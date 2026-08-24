from abc import ABC, abstractmethod


class EstrategiaPrecio(ABC):
    @abstractmethod
    def calcular(self, precio_base: float, cantidad: int) -> float: ...


class PrecioRegular(EstrategiaPrecio):
    def calcular(self, precio_base: float, cantidad: int) -> float:
        return precio_base * cantidad


class PrecioConDescuento(EstrategiaPrecio):
    def __init__(self, porcentaje: float):
        self.porcentaje = porcentaje

    def calcular(self, precio_base: float, cantidad: int) -> float:
        subtotal = precio_base * cantidad
        return subtotal * (1 - self.porcentaje)


class PrecioMayoreo(EstrategiaPrecio):

    def __init__(self, umbral: int, descuento: float):
        self.umbral = umbral
        self.descuento = descuento

    def calcular(self, precio_base: float, cantidad: int) -> float:
        subtotal = precio_base * cantidad
        if cantidad >= self.umbral:
            return subtotal * (1 - self.descuento)
        return subtotal
