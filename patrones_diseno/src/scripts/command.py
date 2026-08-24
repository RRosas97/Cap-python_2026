from abc import ABC, abstractmethod


class Comando(ABC):
    @abstractmethod
    def ejecutar(self) -> None: ...

    @abstractmethod
    def deshacer(self) -> None: ...


class Luz:

    def encender(self) -> None:
        print("  Luz: encendida")

    def apagar(self) -> None:
        print("  Luz: apagada")


class ComandoEncenderLuz(Comando):
    def __init__(self, luz: Luz):
        self._luz = luz

    def ejecutar(self) -> None:
        self._luz.encender()

    def deshacer(self) -> None:
        self._luz.apagar()


class ComandoApagarLuz(Comando):
    def __init__(self, luz: Luz):
        self._luz = luz

    def ejecutar(self) -> None:
        self._luz.apagar()

    def deshacer(self) -> None:
        self._luz.encender()


class ControlRemoto:

    def __init__(self):
        self._historial: list[Comando] = []

    def presionar(self, comando: Comando) -> None:
        comando.ejecutar()
        self._historial.append(comando)

    def deshacer_ultimo(self) -> None:
        if self._historial:
            comando = self._historial.pop()
            comando.deshacer()


if __name__ == "__main__":
    luz = Luz()
    control = ControlRemoto()

    control.presionar(ComandoEncenderLuz(luz))
    control.presionar(ComandoApagarLuz(luz))
    print("Deshaciendo último comando:")
    control.deshacer_ultimo()  # vuelve a encender, porque el último fue "apagar"
