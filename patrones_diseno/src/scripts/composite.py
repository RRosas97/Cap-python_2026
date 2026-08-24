from __future__ import annotations

from abc import ABC, abstractmethod

# Componente: la interfaz común que comparten
#    tanto los objetos individuales como los grupos


class ComponenteMenu(ABC):
    @abstractmethod
    def calcular_precio(self) -> float: ...

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> None: ...


# hoja(leaf) un objeto individual, sin hijos.
#    No sabe nada de "composición", solo es él mismo.


class Producto(ComponenteMenu):
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

    def calcular_precio(self) -> float:
        return self.precio

    def mostrar(self, nivel: int = 0) -> None:
        print("  " * nivel + f"- {self.nombre}: ${self.precio}")


# Composite: Un grupo que contiene OTROS ComponenteMenu,
#    que a su vez pueden ser Productos individuales O más combos.


class ComboMenu(ComponenteMenu):
    def __init__(self, nombre: str, descuento: float = 0.0):
        self.nombre = nombre
        self.descuento = descuento
        self._componentes: list[ComponenteMenu] = []

    def agregar(self, componente: ComponenteMenu) -> "ComboMenu":
        self._componentes.append(componente)
        return self

    def calcular_precio(self) -> float:

        subtotal = sum(c.calcular_precio() for c in self._componentes)
        return subtotal * (1 - self.descuento)

    def mostrar(self, nivel: int = 0) -> None:
        print("  " * nivel + f"+ {self.nombre} (combo, -{self.descuento * 100:.0f}%)")
        for componente in self._componentes:
            componente.mostrar(nivel + 1)


if __name__ == "__main__":
    hamburguesa = Producto("Hamburguesa", 85.0)
    papas = Producto("Papas fritas", 35.0)
    refresco = Producto("Refresco", 25.0)

    combo_clasico = ComboMenu("Combo Clásico", descuento=0.1)
    combo_clasico.agregar(hamburguesa).agregar(papas).agregar(refresco)

    postre = Producto("Helado", 20.0)
    combo_familiar = ComboMenu("Combo Familiar x2", descuento=0.15)
    combo_familiar.agregar(combo_clasico)
    combo_familiar.agregar(postre)

    print("--- Producto individual ---")
    hamburguesa.mostrar()
    print(f"Precio: ${hamburguesa.calcular_precio():.2f}\n")

    print("--- Combo simple ---")
    combo_clasico.mostrar()
    print(f"Precio: ${combo_clasico.calcular_precio():.2f}\n")

    print("--- Combo familiar (con combos anidados adentro) ---")
    combo_familiar.mostrar()
    print(f"Precio: ${combo_familiar.calcular_precio():.2f}")
