from abc import ABC, abstractmethod


class ProcesadorArchivo(ABC):
    def procesar(self, ruta: str) -> None:
        """El "template": define el ORDEN de los pasos, fijo para todos."""
        datos = self.leer(ruta)
        datos_transformados = self.transformar(datos)
        self.guardar(datos_transformados)
        print("  Proceso completo.\n")

    @abstractmethod
    def leer(self, ruta: str) -> str: ...

    @abstractmethod
    def transformar(self, datos: str) -> str: ...

    def guardar(self, datos: str) -> None:
        print(f"  Guardando: {datos}")


class ProcesadorCSV(ProcesadorArchivo):
    def leer(self, ruta: str) -> str:
        print(f"  [CSV] Leyendo {ruta} con csv.DictReader")
        return "nombre,edad\nAna,30"

    def transformar(self, datos: str) -> str:
        return datos.upper()


class ProcesadorJSON(ProcesadorArchivo):
    def leer(self, ruta: str) -> str:
        print(f"  [JSON] Leyendo {ruta} con json.load")
        return '{"nombre": "Ana", "edad": 30}'

    def transformar(self, datos: str) -> str:
        return datos.replace(":", " ->")

    def guardar(self, datos: str) -> None:
        print(f"  [JSON] Guardando con formato especial: {datos}")


if __name__ == "__main__":
    print("Procesando CSV:")
    ProcesadorCSV().procesar("datos.csv")

    print("Procesando JSON:")
    ProcesadorJSON().procesar("datos.json")
