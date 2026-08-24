import time
from abc import ABC, abstractmethod


class ServicioReportes(ABC):
    @abstractmethod
    def obtener_reporte(self, id_reporte: str) -> str: ...


class ServicioReportesReal(ServicioReportes):

    def obtener_reporte(self, id_reporte: str) -> str:
        print(f"  [Real] Generando reporte {id_reporte} (operación costosa)...")
        time.sleep(1)
        return f"Contenido del reporte {id_reporte}"


class ServicioReportesProxy(ServicioReportes):

    def __init__(self, servicio_real: ServicioReportesReal):
        self._servicio_real = servicio_real
        self._cache: dict[str, str] = {}

    def obtener_reporte(self, id_reporte: str) -> str:
        if id_reporte in self._cache:
            print(f"  [Proxy] Devolviendo {id_reporte} desde caché, sin llamar al real")
            return self._cache[id_reporte]

        resultado = self._servicio_real.obtener_reporte(id_reporte)
        self._cache[id_reporte] = resultado
        return resultado


if __name__ == "__main__":
    proxy = ServicioReportesProxy(ServicioReportesReal())

    inicio = time.perf_counter()
    proxy.obtener_reporte("Q3")
    proxy.obtener_reporte("Q3")
    print(f"Tiempo total: {time.perf_counter() - inicio:.2f}s")
