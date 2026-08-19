import time


class Timer:
    def __enter__(self):
        self.initial_time = time.time()
        print("Entré al bloque.")

    def __exit__(self, exc_type, exc, tb):
        print("Saliendo del bloque")
        final_time = time.time()
        print(final_time - self.initial_time)


with Timer():
    print("Estoy dentro")
