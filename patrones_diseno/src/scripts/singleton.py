class Configuracion:  # Atributo de clase: almacena la única instancia permitida.
    _instancia = None

    # Bandera para evitar ejecutar la inicialización más de una vez.
    _inicializada = False

    def __new__(cls, *args, **kwargs):
        """
        __new__ se ejecuta antes de __init__.
        Aquí se crea o se devuelve la única instancia de la clase.
        """
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)

        # Si ya había una instancia, se devuelve esa misma instancia.
        return cls._instancia

    def __init__(self, host: str = "localhost", puerto: int = 5432):
        """
        Aunque __new__ devuelva la misma instancia, Python invoca __init__
        cada vez que se escribe Configuracion(...).
        La bandera evita sobrescribir la configuración original.
        """
        if self._inicializada:
            return

        self.host = host
        self.puerto = puerto
        self._inicializada = True

    def mostrar(self) -> None:
        print(f"Host: {self.host}")
        print(f"Puerto: {self.puerto}")


# Se crea la primera instancia y se inicializa con estos valores.

config_1 = Configuracion("servidor-produccion", 1433)

# Parece que se crea otra instancia, pero new devuelve config_1.

# Además, init no modifica host ni puerto gracias a _inicializada.

config_2 = Configuracion("otro-servidor", 9999)

# is comprueba si ambas variables apuntan exactamente al mismo objeto.

print(config_1 is config_2)  # True

# Los datos conservan los valores de la primera inicialización.

config_1.mostrar()

# También se puede verificar que ambas referencias muestran lo mismo.

config_2.mostrar()
