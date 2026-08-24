from __future__ import annotations

from dataclasses import dataclass, field

# Producto: el objeto complejo que queremos construir


@dataclass
class Computadora:
    cpu: str = ""
    ram_gb: int = 0
    disco_gb: int = 0
    gpu: str | None = None
    perifericos: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        partes = [
            f"CPU: {self.cpu}",
            f"RAM: {self.ram_gb}GB",
            f"Disco: {self.disco_gb}GB",
            f"GPU: {self.gpu or 'integrada'}",
            f"Periféricos: {', '.join(self.perifericos) or 'ninguno'}",
        ]
        return " | ".join(partes)


# Builder: construye el producto PASO A PASO,
#    devolviendo "self" en cada paso para poder encadenar llamadas


class ComputadoraBuilder:
    def __init__(self):
        self._computadora = Computadora()

    def con_cpu(self, cpu: str) -> "ComputadoraBuilder":
        self._computadora.cpu = cpu
        return self  # <- esto es lo que permite encadenar .con_cpu(...).con_ram(...)

    def con_ram(self, gb: int) -> "ComputadoraBuilder":
        self._computadora.ram_gb = gb
        return self

    def con_disco(self, gb: int) -> "ComputadoraBuilder":
        self._computadora.disco_gb = gb
        return self

    def con_gpu(self, gpu: str) -> "ComputadoraBuilder":
        self._computadora.gpu = gpu
        return self

    def agregar_periferico(self, nombre: str) -> "ComputadoraBuilder":
        self._computadora.perifericos.append(nombre)
        return self

    def build(self) -> Computadora:
        """Entrega el producto terminado y reinicia el builder para la siguiente
        construcción."""
        resultado = self._computadora
        self._computadora = Computadora()
        return resultado


# Director: conoce "recetas" completas,
#    para no repetir la misma secuencia de pasos en cada lugar del código


class ComputadoraDirector:
    def __init__(self, builder: ComputadoraBuilder):
        self._builder = builder

    def construir_pc_oficina(self) -> Computadora:
        return self._builder.con_cpu("Intel i5").con_ram(8).con_disco(256).build()

    def construir_pc_gaming(self) -> Computadora:
        return (
            self._builder.con_cpu("AMD Ryzen 9")
            .con_ram(32)
            .con_disco(1000)
            .con_gpu("RTX 4080")
            .agregar_periferico("teclado mecánico")
            .agregar_periferico("mouse gamer")
            .build()
        )


if __name__ == "__main__":

    pc_personalizada = (
        ComputadoraBuilder()
        .con_cpu("AMD Ryzen 5")
        .con_ram(16)
        .con_disco(512)
        .agregar_periferico("monitor extra")
        .build()
    )
    print("PC personalizada:", pc_personalizada)

    builder = ComputadoraBuilder()
    director = ComputadoraDirector(builder)

    pc_oficina = director.construir_pc_oficina()
    print("PC oficina: ", pc_oficina)

    pc_gaming = director.construir_pc_gaming()
    print("PC gaming: ", pc_gaming)
