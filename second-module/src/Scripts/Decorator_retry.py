import random
import time


def reintentar(intentos_max, espera):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for i in range(intentos_max):
                try:
                    result = func(*args, **kwargs)
                    return result
                except ValueError:
                    nonlocal espera
                    time.sleep(espera)
                    espera = espera * 2
            raise ValueError(f"Falló después de {intentos_max} intentos.")

        return wrapper

    return decorador


def funcion_que_a_veces_falla():
    if random.random() < 0.7:
        raise ValueError("Algo salió mal")
    return "Éxito"


@reintentar(intentos_max=4, espera=1)
def tarea():
    return funcion_que_a_veces_falla()


print(tarea())
