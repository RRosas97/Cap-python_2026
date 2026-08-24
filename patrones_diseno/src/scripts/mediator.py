from abc import ABC, abstractmethod


class SalaChat(ABC):
    @abstractmethod
    def enviar_mensaje(self, mensaje: str, remitente: "Usuario") -> None: ...


class SalaChatConcreta(SalaChat):

    def __init__(self):
        self._usuarios: list[Usuario] = []

    def unirse(self, usuario: "Usuario") -> None:
        self._usuarios.append(usuario)

    def enviar_mensaje(self, mensaje: str, remitente: "Usuario") -> None:
        for usuario in self._usuarios:
            if usuario is not remitente:
                usuario.recibir(mensaje, remitente.nombre)


class Usuario:
    def __init__(self, nombre: str, sala: SalaChat):
        self.nombre = nombre
        self._sala = sala

    def enviar(self, mensaje: str) -> None:
        print(f"{self.nombre} envía: {mensaje}")
        self._sala.enviar_mensaje(mensaje, self)

    def recibir(self, mensaje: str, de: str) -> None:
        print(f"  {self.nombre} recibe de {de}: {mensaje}")


if __name__ == "__main__":
    sala = SalaChatConcreta()

    ana = Usuario("Ana", sala)
    luis = Usuario("Luis", sala)
    marco = Usuario("Marco", sala)

    sala.unirse(ana)
    sala.unirse(luis)
    sala.unirse(marco)

    ana.enviar("Hola a todos")
