import time
from functools import wraps


def cache_con_ttl(segundos: float):

    def decorador(func):
        cache: dict[tuple, tuple[float, object]] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            clave = (args, tuple(sorted(kwargs.items())))
            ahora = time.time()

            if clave in cache:
                timestamp, resultado = cache[clave]
                if ahora - timestamp < segundos:
                    print(f"  [cache] HIT para {args[1:]}")
                    return resultado

            print(f"  [cache] MISS para {args[1:]}, consultando de verdad")
            resultado = func(*args, **kwargs)
            cache[clave] = (ahora, resultado)
            return resultado

        wrapper.cache_info = lambda: cache
        return wrapper

    return decorador
